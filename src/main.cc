#include <QApplication>
#include <QPushButton>

#include "main_window.h"

int main(int argc, char *argv[]) {
	QApplication a(argc, argv);
	MainWindow window(nullptr);
	window.resize(700, 400);
	window.show();
	return QApplication::exec();
}
