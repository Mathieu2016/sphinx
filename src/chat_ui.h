//
// Created by carl on 23-5-26.
//

#ifndef SPHINX_CHAT_UI_H
#define SPHINX_CHAT_UI_H

#include <QWidget>
#include <QLayout>
#include <QTextEdit>
#include <QPushButton>
#include <QLineEdit>
#include <QString>
#include <QtNetwork/QNetworkRequest>
#include <QtNetwork/QNetworkAccessManager>
#include <QtNetwork/QNetworkReply>
#include <QEventLoop>


class ChatUi : public QWidget {
public:
	explicit ChatUi(QWidget *parent = nullptr);
private:
	QGridLayout *chat_layout_;
	QTextEdit *display_text_;
	QLineEdit *content_edit_;
	QPushButton *mode_switch_;
	QPushButton *send_;
	QNetworkAccessManager *network_manager_;

	void SendChatContent();
	void HandleReply(QNetworkReply *reply);
};

#endif //SPHINX_CHAT_UI_H
