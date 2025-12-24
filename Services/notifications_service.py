def print_notifications(notifications: list):
    print("---")
    for i, notification in enumerate(notifications):
        type_id = notification["typeId"]
        text = ""
        match type_id:
            case 1:
                text = f"{i + 1}. Важное уведомление"
            case 2:
                text = f"{i + 1}. Ваш заказ взят в работу"
            case 3:
                text = f"{i + 1}. Ваш заказ завершен"
            case 4:
                text = f"{i + 1}. Вам оставили отзыв"
            case 5:
                text = f"{i + 1}. Вы завершили заказ, оставьте отзыв о клиенте"
        if not notification["isRead"]:
            text += " !"
        print(text)
        print("---")
