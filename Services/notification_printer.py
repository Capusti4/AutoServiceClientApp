def print_notifications(notifications):
    for i, notification in enumerate(notifications):
        type_id = notification["typeId"]
        match type_id:
            case 1:
                print(f"{i + 1}. Важное уведомление")
            case 2:
                print(f"{i + 1}. Ваш заказ взят в работу")
            case 3:
                print(f"{i + 1}. Ваш заказ завершен")
        print("---")