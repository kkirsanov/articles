#include <Python.h>
#include <boost/python.hpp>

int add_five(int x) {return x + 5;}
BOOST_PYTHON_MODULE(Test){
   def("add_five", add_five);
}

int main(){
  Py_Initialize();
  initTest();
  PyRun_SimpleString("import Test");
  PyRun_SimpleString("print Test.add_five(4)");
  return 0;
}
