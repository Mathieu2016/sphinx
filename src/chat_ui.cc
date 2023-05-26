//
// Created by carl on 23-5-26.
//

#include "chat_ui.h"

ChatUi::ChatUi(QWidget *parent) {
	chat_layout_ = new QGridLayout(this);
	display_text_ = new QTextEdit(this);
	content_edit_ = new QLineEdit(this);
	mode_switch_ = new QPushButton(this);
	network_manager_ = new QNetworkAccessManager(this);
	send_ = new QPushButton(this);

	mode_switch_->setText("切换");
	send_->setText("发送");

	chat_layout_->addWidget(display_text_, 0, 0, 3, 5);
	chat_layout_->addWidget(mode_switch_, 3, 0, 1, 1);
	chat_layout_->addWidget(content_edit_, 3, 1, 1, 3);
	chat_layout_->addWidget(send_, 3, 4, 1, 1);

	connect(send_, &QPushButton::clicked, this, &ChatUi::SendChatContent);
	connect(network_manager_, &QNetworkAccessManager::finished, this, &ChatUi::HandleReply);

	this->setLayout(chat_layout_);
}

void ChatUi::SendChatContent() {
	QNetworkRequest request;

	request.setUrl(QUrl("http://localhost:8000"));

	QNetworkReply *reply =  network_manager_->get(request);

	QEventLoop loop;
	connect(reply, &QNetworkReply::finished, &loop, &QEventLoop::quit);
	loop.exec();
}

void ChatUi::HandleReply(QNetworkReply *reply) {
	QString res = reply->readAll();
	display_text_->append(res);
	// qDebug() << "received reply: " << res ;
}

