# Task description


# Solution description
## Требования
1. Каждый комментарий имеет привязку к определенному пользователю.
2. У каждого комментария есть дата создания.
3. Коментарии имеют древовидную структуру - есть возможность оставлять
комментарии на комментарии с неограниченной степенью вложенности.
4. Каждой комментарий имеет привязку к определенной сущности (пост в блоге,
страница пользователя, другой комментарий и т.п.), которая однозначно
идентифицируется парой значений (идентификатор типа сущности,
идентификатор сущности).
5. Бэкенд должен предоставлять следующие интерфейсы:
    1. Создание комментария к определенной сущности с указанием
сущности, к которой он относится.
    2. Получение комментариев первого уровня для определенной
сущности с пагинацией.
    3. Получение всех дочерних комментариев для заданного
комментария или сущности без ограничения по уровню
вложенности. Корнем может являться пара идентифицирующая
сущность или id комментария, являющегося корневым для данной
ветки. Ответ должен быть таким, чтобы на клиенте можно было
воссоздать иерархию комментариев.
    4. Получение истории комментариев определенного пользователя.
    5. Выгрузка в файл (например в xml-формате) всей истории
комментариев по пользователю или сущности с возможностью
указания интервала времени, в котором был создан комментарий
пользователя (если не задан - выводить всё). Время ответа на
первичный запрос не должно зависеть от объема данных в
итоговой выгрузке.
6. Время ответа на все запросы ограничено 1 секундной. С условием:
    1. глубина дерева не менее 100,
    2. количество узлов (элементов, имеющих дочерние элементы) в дереве
не менее 10^4.

## Дополнительные требования
1. Комментарии могут редактироваться и удаляться. Удаление возможно только,
если у комментария нет дочерних комментариев. Реализовать хранение
исторических данных с возможностью получения истории для определенного
комментария: информация о том, кем и когда был изменен/удален
комментарий, что изменилось в комментарии.
2. Возможность подписки на события комментирования определенной сущности -
при создании/редактировании/удалении комментария к этой сущности с
сервера уходит PUSH-уведомление клиенту с информацией о
созданном/отредактированным/удаленным комментарием в таком виде, чтобы
клиент имел возможность динамически добавить/обновить/удалить его в
интерфейсе.
3. Для пункта 5.v требований реализовать гибкий механизм с возможностью
добавления различных форматов файлов


 ## Описание решения.
Приложение предоставляет REST API для работы с сервисом комментариев. 

Используемые технические средства: 
* python 3.6, 
* dgango rest framework, 
* Django framework

В данном решении для комментирования доступны следующие сущности:
* Страница (`Page`)
* Пост (`Post`)
* Комментарий(`Comment`)

Предложенная архитектура (композиция с `Entity`) позволяет быстро добавлять новые сущности для комментирования.
Подписка на события реальзована с использованием библиотеки `django-channels`, позволяющей отправлять `PUSH` уведовмления с сервера. 

Для выгрузки в файл всей истории комментариев используется асинхронная задача, которая обрабатыввается в `celery`. В ответ на запрос пользователь получает идентификатор задачи, после выполнения которой будет отправлено PUSH-сообщение c `url` сформированного файла. Подписка на события должна осуществляться по идентификатору задачи.
В качестве альтернативного варианта системы очередей задач можно было бы использовать библиотеку `Channels`.  Однако согласно документации `Channels` не гарантирует выполнение задачи, так как отсутствует failover/retry механизм:
_Channels’ design is such that anything is allowed to fail - a consumer can error and not send replies, the channel layer can restart and drop a few messages, a dogpile can happen and a few incoming clients get rejected._

Для добавления различных форматов файлов для пункта 5.v осудествляется посредством расширения словаря форматов `ext_serializer_dict` функции `get_history` и реализации соответствующих сериалайзеров данных. 
Возможность добавления дополнительных средств обработки сериализованных данных перед сохранением в файл, путем расширения словаря `ext_dict` задачи `save_history_to_fil` расширяет возможности обработки данных.

### Описание методов
1.Методы для работа с комментариями
   
   + application_url/comments/
   
        - **GET** - the list of all comments in the system, excluding deleted
        - **POST** - create a new comment 
       
       Request example:
       ```json
       {
            "entity": {
                "user": 1,
                "date": "2017-10-08T12:34:48Z"
            },
            "to": 1,
            "text": "text"
        }
       ```
    
   + application_url/comments/comment/(?P<pk>[0-9]+)/
    
	   - **GET** - return the not deleted comment information by id
	   - **PUT** - update a not deleted comment by id
	   - **PATCH** - partially update a not deleted comment by id
	    
	    Request example:
       ```json
       {
            "text": "Edited text"
        }
       ```
	   - **DELETE** - mark the comment as deleted by id
   
   + application_url/comments/top_comments/ 
    
	   - **GET** - provides the list of top level comments
   
   + application_url/comments/inherited_comments/(?P<id>[0-9]+)/(?P<type>["comment", "post", "page"]+)/$
    
	   - **GET** - provides the list inherited comments of given object, where **id** is object id and **type** is type of the object (possible arguments are "comment", "post" and "page")
   
   + application_url/comments/user_history/$
   
	  - **POST** - provides the history of user's comments
      
        POST arguments:
    
        - **user_id**: ID of the user
        - **with_deleted**: if equals to true or 1 then the response
        contains both deleted and not deleted comments and only not deleted
        comments otherwise
        
   
   + application_url/comments/store_history/$
    
	   - **POST** - store user history or comment history information into the file
        
            POST arguments:
        
            - **id**: ID of an object
            - **model**: object model name [comment|post|page|user]
            - **date_from**: look date_to
            - **date_to**: not required param to filter results by creation dates
            - **with_deleted**: if equals to true or 1 then the response contains both deleted and not deleted comments and only not deleted comments otherwise
            - **format**: file format to store data to 
 
 2. Методы для работы с историей изменений  
   + application_url/history/
   
	   - **GET** - the list of all history records in system
    
  
   + application_url/history/^(?P<comment_id>[0-9]+)/
   
	   - **GET** - the list of all comment history records by comment ID
  
3.Методы для работы со страницами 
   
   + application_url/pages/
	   - **GET** - the list of all pages
	   - **POST** - create a new page
	   
	    Request example:
       ```json
       {
            "caption": "Test page",
            "entity": {
                "user": 1,
                "date": "2012-03-22T11:12:00Z"
            }
        }

       ```
	   
   + application_url/pages/page/(?P<pk>[0-9]+)/
   
	   - **GET** - return a page information by id
	   - **PUT** - update a page by id
	   - **PATCH** - partially update a page by id
	   - **DELETE** - delete a page by id
    
    
4.Методы для работы с постами
    
   + application_url/posts/
   
	   -  **GET** - the list of all posts
	   -  **POST** - create a new post
	   
	   Request example:
       ```json
       {
            "caption": "Test post",
            "entity": {
                "user": 1,
                "date": "2012-03-22T11:12:00Z"
            }
        }

    
   + application_url/posts/post/(?P<pk>[0-9]+)/
    
	    - **GET** - return a post information by id
        - **PUT** - update a post by id
        - **PATCH** - partially update a post by id
        - **DELETE** - delete a post by id


## Запуск
Для запуска приложения выполните слудующие команды в консоли в папке проекта
```
cp config_default.ini config.ini
docker-compose build
docker-compose up -d
docker-compose exec app python manage.py createsuperuser # следовать инструкциям терминала
```
Проект будет запущен на порту [8080](http://localhost:8080/comments)
