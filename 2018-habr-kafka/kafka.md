# Опыт построения инфраструктуры на микросервисной архитектуре

В статье описывается опыт перевода крупной финтех python инфраструктуры состоящей из нескольких монолитных приложений связанных синхронными протоколами на микросервисную архитектуру

<cut />

## Откуда идём и куда хотим придти

У нас в небольшом банке были большие проблемы: монструозное монолитное python приложение из 4-5 отдельных кусков (один даже на php) связанных чудовищным количесвтом синхронных RPC взаимодейсвий с большим объемом legacy. Разрабатывать, тестировать, выкладывать, администрировать, поддреживать, смотреть логи - всё тяжело, долго и неудобно. Так жизнь нельзя, а как жить нужно ещё требуется определить. Крупными мазками определили:

- нужны микросервисы
- ими нужно управлять (сначала был nomad, но после года использования перешли на k8s)
- их нужно мониторить (уже был заббикс, затем появились influxdb, prometheus, grafana)

Дальнейшее изложение будет сосредоточено вокруг микросеривсов

понятная и простая технология масштабирования
возможность повторного прогона задний
асинхронность