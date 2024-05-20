with open('user.txt', 'r') as file:
    data_in_file = file.readlines()
print(data_in_file)
# if not str(message.chat.id) + '/n' in data_in_file:
#     with open('user.txt', 'a') as file:
#         print(str(message.chat.id), file=file)