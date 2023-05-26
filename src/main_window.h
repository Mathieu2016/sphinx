//
// Created by carl on 23-5-26.
//

#ifndef SPHINX_MAIN_WINDOW_H
#define SPHINX_MAIN_WINDOW_H

#include <QMainWindow>
#include "chat_ui.h"

class MainWindow : public QMainWindow {
public:
	MainWindow(QWidget *parent = nullptr);
	~MainWindow();

	ChatUi *chat_ui_;
};

#endif //SPHINX_MAIN_WINDOW_H
