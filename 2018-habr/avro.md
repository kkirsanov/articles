![](https://habrastorage.org/webt/z-/0e/wd/z-0ewdccnmr67afgrhvkkxfvjxk.png)

В статье описывается использование формата сериализации AVRO в языке pyhon с помощью библиотеки fastavro, дается краткое описание AVRO-схемы с пояснениями наиболее неочевидных момоентов, приводятся конкретные примеры кода на python.

Намеренно исключены из рассмотрения вопросы эволюции схем (schema evolution), RPC и AVRO-IDL.
<cut />

### Историческая справка

Почему AVRO, а не json, bson, msgpack, protobuf, ASN.1, thrift, yaml?

При декомпозиции монолитной системы возникла необходимость описать процедуру взаимодействия между микросервисами. Не долго выбирая между RabbitMQ и Kafka остановились на последней. Но вот над следующей задачей - выборе системы сериализации пришлось попотеть.

При выборе системы сериализации учитывались следующие требования:

1. Поддержка нескольких языков программирования

    Основа нашей кодовой базы - python 2.7. При чем в дальнейшем хотелось бы чувствительные к производительности процессы перевести на другие языки.

2. Валидация данных при сериализации

    В динамическом интерпретируемом питоне слишком просто случайно отправить "не те" данные. А в выбранной нами pub-sub модели кафки нам было очень важно обеспечить корректность входных данных в топике. Нужна была система позволяющая типизировать топики кафки.

3. Поддержка типов

    Наша система активно оперирует типами Decimal, UUID и Datetime. Увы - известные форматы сериализации начиная ASN.1 и заканчивая msgpack в основном описывают сериализацию низкоуровневых типов (int\float\string\bytes) и не предлагают законченных решений для интересующих нас.

Исходя из этих соображений выбор пал на AVRO. Но внезапно оказалось (весна 2017)  что  не смотря на наличие поддержки логических типов в [спецификации](http://avro.apache.org/docs/current/spec.html#Logical+Types) и JAVA билиотеки - ни в [официальной](https://pypi.python.org/pypi/avro/1.8.2) реализации AVRO для python, ни в конкурирующей [fastavto](https://github.com/tebeka/fastavro/) их просто проигнорировали. Пришлось добавлять самостоятельно.

Наиболее адекватный (а также самый быстрый) код оказался у fastavro, в результате было принято решение доработать эту библиотеку. Это стало первым моим опытом участия в opensource.

# Что такое AVRO

AVRO это система сериализации данных, созданная в рамках проекта Hadoop. Данные сериализуются бинарный формат с помощью предварительно созданной json-схемы при чем для десериализации также требуется схема (возможно - другая).

Также AVRO позволят в рамках одного контейнера упаковать множество записей заданных единственной схемой, что позволяет эффективно передавать большие объемы данных, избегая свойственные другим форматам накладные расходы.

## AVRO-схема

Я не стану подробно описывать правила построения схем, т.к. они изложены в [официальной документации](http://avro.apache.org/docs/current/spec.html)
Остановлюсь лишь на базовых вещах и совсем уж не очевидных моментах.

AVRO-схема представляет из себя JSON, описывающий сериализуемую\десериализуемую структуру данных. Типы данных могут быть:

1. Примитивными
    * *null*
    * *boolean*
    * *int* - знаковое целое 32 бита
    * *long* - знаковое целое 64 бита
    * *float*
    * *double*
    * *string* - unicode строка
    * *bytes* - последовательность байт
    * *fixed* - те же байты, но с длинной заданной в схеме
2. Составными
    * union - тип-сумма
    * *recod* - тип-произведение
    * *enum* - перечисление
    * *array* - массив/список
    * *map* - ассоциативный массив
3. Логическими (в терминологии AVRO)
    * *decimal* - число с фиксированной точкой
    * *date* - дата
    * *time-millis* - время с миллисекундной точностью
    * *time-micros* - время с микросекундной точностью
    * *timestamp-millis* - дата-время с миллисекундной точностью
    * *timestamp-micros* - дата-время с микросекундной точностью
    * *uuid* - universally unique identifier

Хотя вышеперечисленные логические типы уже давно являются стандартом в реляционных БД и современных языках программирования - библиотеки сериализации обходили их стороной, вынуждая сводить их к примитивным типам, к счастью в AVRO эта проблема решена.

Рассмотрим простую схему:

```json
{
  "type": "record",
  "namespace": "notificator",
  "name": "out",
  "doc": "HTTP нотификация",
  "fields": [
    {
      "doc": "id задания",
      "name": "id",
      "type": "long"
    },
    {
      "name": "datetime",
      "doc": "время постановки задания",
      "type": {
        "type": "long",
        "logicalType": "timestamp-millis"
      }
    },
    {
      "doc": "источник нотификации",
      "name": "source",
      "type": [
        "null",
        "string"
      ]
    },
    {
      "doc": "Метод",
      "name": "method",
      "default": "POST",
      "type": {
        "type": "enum",
        "name": "methods",
        "symbols": [
          "POST",
          "GET",
        ]
      }
    },
    {
      "name": "url",
      "type": "string"
    },
    {
      "name": "headers",
      "type": {
        "type": "map",
        "values": "string"
      }
    },
    {
      "doc": "body",
      "name": "body",
      "type": "bytes"
    }
  ]
}
```

Схема начинается с объявления типа record с заданными name и namespace. Эти поля в первых строках будут использоваться в системах кодогенерации, не актуальных для питона, т.к. у нас схема будет обрабатываться динамически. Далее идет перечисление типов полей нашей записи.

Особый интерес представляет объявление поля datetime, т.к. оно содержит логический тип. Важно помнить, что **логические типы следует задавать вложенными в описания типа поля**.

неправильно:

```json
{
    "name": "datetime",
    "doc": "время постановки задания",
    "type": "long",
    "logicalType": "timestamp-millis"
},
```

правильно:

```json
{
    "name": "datetime",
    "doc": "время постановки задания",
    "type": {
        "type": "long",
        "logicalType": "timestamp-millis"
    }
},
```

Далее идет поле source объявленное как union ```"type": ["null", "string"]```, эта запись означает что значение source может быть одного из двух типов ```null``` или ```string```. Комбинировать таким образом можно не только примитивные типы, но и составные и логические. Примеры таких комбинаций, а также более сложных схем можно посмотреть [тут](https://github.com/tebeka/fastavro/blob/master/tests/test_complex.py)
Ещё один неочевидный момент связан с ```default```: **значение по умолчанию должно быть задано для первого типа в перечислении**.

неправильно:

```json
{
      "name": "f",
      "type": ["long", "string"],
      "default": "asd"
    },
```

правильно:

```json
{
      "name": "f",
      "type": ["string", "long"],
      "default": "asd"
    },
```

Отдельного упоминания заслуживают логические типы Decimal (число с фиксированной точкой) и UUID.

Decimal требует дополнительных параметров - числа знаков в числе и числа знаков после запятой:

```json
 {
    "name": "money",
    "doc": "16 знаков, 4 после точки",
    "type": {
        "type": "bytes",
        "logicalType": "decimal",
        "precision": 16,
        "scale": 4,
    }
}
```

А UUID интересен тем, что в спецификации его нет, а реализация его [есть](https://github.com/apache/avro/blob/17f2d75132021fafeca29edbdcade40df960fdc9/lang/java/avro/src/main/java/org/apache/avro/Conversions.java#L52). При чём довольно странно сделанная - UUID кодируется строкой.

```json
{
    "name": "uuid",
    "type": {
        "type": "string",
        "logicalType": "uuid"
    }
}
```

Пришлось добавить в fastavro и такую реализацию.

# Примеры работы с fastavro

### Как прочитать из контейнера
```python
import fastavro as avro

with open('some-file.avro', 'rb') as fo:
    # можно подменить схему контейнера с помощью reader_schema
    reader = fastavro.reader(fo, reader_schema=None)
    schema = reader.schema

    for record in reader:
        process_record(record)
```

### Как записать в контейнер
```python
from fastavro import writer

schema = {
    'doc': 'A weather reading.',
    'name': 'Weather',
    'namespace': 'test',
    'type': 'record',
    'fields': [
        {'name': 'station', 'type': 'string'},
        {'name': 'time', 'type': 'long'},
        {'name': 'temp', 'type': 'int'},
    ],
}

records = [
    {'station': '011990-99999', 'temp': 0, 'time': 1433269388},
    {'station': '011990-99999', 'temp': 22, 'time': 1433270389},
    {'station': '011990-99999', 'temp': -11, 'time': 1433273379},
    {'station': '012650-99999', 'temp': 111, 'time': 1433275478},
]

with open('weather.avro', 'wb') as out:
    writer(out, schema, records)
```

### Как сериализовать и десериализовать данные вне контейнера

Используется при передачи данных как сообщений.

```python
from io import BytesIO
import fastavro

def serialize(schema, data):
    bytes_writer = BytesIO()
    fastavro.schemaless_writer(bytes_writer, schema, data)
    return bytes_writer.getvalue()

def deserialize(schema, binary):
    bytes_writer = BytesIO()
    bytes_writer.write(binary)
    bytes_writer.seek(0)

    data = fastavro.schemaless_reader(bytes_writer, schema)
    return data
```

### Как подавить чтение логических типов

```python
import fastavro
fastavro._reader.LOGICAL_READERS['long-timestamp-millis'] = lambda d, w, r: d
```

Теперь логический тип timestamp-millis будет читаться не в Datetime питона, а в long.

### Как заранее прочитать схему

В fastavro предусмотрена функция acquaint_schema, которая считывает схему во внутренний репозиторий (бывают ещё и [внешение](https://docs.confluent.io/current/schema-registry/docs/intro.html), но это отдельная история).

Имея схему

```json
{
  "name": "decimal_18_6",
  "namespace": "types",
  "type": "bytes",
  "logicalType": "decimal",
  "precision": 18,
  "scale": 6
}
```

и загрузив её с помощью acquaint_schema можно в дальнейшем использовать краткое описание типов :

```json
"fields": [
    {
        "name": "money1",
        "type": "types.decimal_18_6"
    },
    {
        "name": "money2",
        "type": "types.decimal_18_6"
    },
]
```

*Обратите внимание - имя типа при обращении включает его namespace **types**.decimal_18_6*

Также это необходимо в отдельных [не тривиальных случаях](https://github.com/tebeka/fastavro/issues/101)