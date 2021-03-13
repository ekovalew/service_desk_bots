# service_desk_bots
Боты для vk.com и telegram, отвечающие на типовые вопросы пользователей в тех. поддержку. Боты построены на основе DialogFlow. 
DialogFlow - это облачный сервис распознавания естественного языка от Google.
# Примеры работы ботов
![demo_vk_bot](https://user-images.githubusercontent.com/49534555/111034741-1c1aaa80-8428-11eb-8913-fb707ff5a0b6.gif)
![demo_tg_bot](https://user-images.githubusercontent.com/49534555/111034745-1d4bd780-8428-11eb-8103-1ec76aa904c5.gif)

# Деплой
- создать аккаунт в DialogFlow и проект в нём (https://cloud.google.com/dialogflow/es/docs/quick/setup);
- создать Агента (https://cloud.google.com/dialogflow/es/docs/quick/build-agent);
- создать новый Intent (заполнить Training phrases и Response);
- в Google Cloud Control в разделе APIs&Services создать json с ключами для подключения по API через CREATE CREDENTIALS;
- добавить json в heroku в Config Vars (https://stackoverflow.com/questions/47446480/how-to-use-google-api-credentials-json-on-heroku);
- добавить билдпак (https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack);
- добавить билдпак heroku/python (должен быть вторым в разделе Buildpacks);
- подключить репозиторий https://github.com/ekovalew/service_desk_bots во вкладке Deploy;
- включить ботов в Resources.
