//
// Created by carl on 23-5-26.
//

#include "main_window.h"

MainWindow::MainWindow(QWidget *parent) {
	chat_ui_ = new ChatUi(parent);

	setCentralWidget(chat_ui_);
}

MainWindow::~MainWindow() noexcept = default;