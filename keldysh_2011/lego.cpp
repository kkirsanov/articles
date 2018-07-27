#include "Lcd.h"
using namespace ecrobot;
extern "C" {
#include "ecrobot_interface.h"
void user_1ms_isr_type2(void) {
}
TASK(TaskMain)
{
	Lcd lcd;
	lcd.clear();
	lcd.putf("s", "Hello World");
	lcd.disp();
	while(1);
}
}
