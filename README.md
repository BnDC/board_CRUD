# board_CRUD
<br>

## core app
### model
- 이력관리를 위한 created_at, updated_at, deleted_at를 가진 
TimeStampModel을 만들어 다른 model에 상속시켰습니다.

<br>

### view
- 로그인이 필요한 요청에 앞서 로그인 상태를 확인 할 수 있는
loginz-decorator함수 login_required를 만들었습니다.

<br><br><br>
## user app

### model
- email, password, nickname field를 가진 User model을 만들었습니다.

<br>

### view
#### SignupView 
(POST)
- 등록하려는 email과 nickname이 db에 있는지 확인하였습니다
- 정규 표현식을 이용해 email형식과 password의 조건(영문, 숫자, 특수문자 필수 입력된 8~20자)을 만족하는지 검사했습니다.
- bcrypt를 이용해 password를 암호화 하였습니다.
- 전달 받은 key값을 확인하고, 약속된 key값이 맞으면 key값의 value로 user 데이터를 저장해 회원가입을 완료하였습니다. 


#### LoginView
(POST)
- 입력받은 email을 가진 user가 있는지 확인하였습니다.
- bcrypt를 이용해 입력받은 password의 hash값과 db에 저장된 password hash 값을 비교해 password를 확인하였습니다. 
- pyjwt를 이용해 access_token을 생성하여 전달하였습니다.

<br><br><br>
## posting app

### model
- title, content를 field로 가진 posting model을 만들었습니다. 
- posting model은 user id를 참조하여 user와 posting을 1:N 관계로 설정하였습니다.

<br>

### view
#### PostingView
(POST)
- login_required를 이용해 로그인한 사용자인지 확인하였습니다.
- 전달 받은 key값을 확인하고, 약속된 key값이 맞으면 key값의 value로 posting 데이터를 저장해 께시판 글 작성을 완료하였습니다.

(GET)
- 전달 받은 posting_id를 확인하고, db에 존재하는 게시글인지 확인하였습니다.
- deleted_at의 값을 확인해 게시글이 삭제되었는지 확인하였습니다.
- 존재하는 게시글이라면 게시글의 정보를 보내주었습니다.

(PATCH)
- 전달 받은 posting_id를 확인하고, db에 존재하는 게시글인지 확인하였습니다.
- deleted_at의 값을 확인해 게시글이 삭제되었는지 확인하였습니다.
- posing을 작성한 user가 맞는지 확인하였습니다.
- 존재하는 게시글이고 로그인한 사용자가 작성자가 맞으면 요청 받은 수정사항을 db에 반영하였습니다.

(DELETE)
- 전달 받은 posting_id를 확인하고, db에 존재하는 게시글인지 확인하였습니다.
- deleted_at의 값을 확인해 게시글이 삭제되었는지 확인하였습니다.
- posing을 작성한 user가 맞는지 확인하였습니다.
- 존재하는 게시글이고 로그인한 사용자가 작성자가 맞으면 deleted_at을 현재시간으로 update함으로, soft delete 하였습니다.

<br>

### PostingListView
(GET)
- query parameter를 통해 page 정보를 받고, paginator를 이용해
전체 posting을 page별로 5개 씩 나누어 보내 주었습니다. 


<br><br><br><br><br>

# endpoint

POST /users/signup <br>
POST /users/login

POST /postings <br>
GET /postings/list?page=1  <br>
GET /postings/\<int:posting_id\> <br>
PATCH /postings/\<int:posting_id\> <br>
DELETE /postings/\<int:posting_id\>

<br><br><br><br><br>

# API 명세서

## POST 회원가입 API
http://127.0.0.1:8000/users/signup

<br>

### request

#### HEADERS

POST /users/signup HTTP/1.1 <br>
Accept: application/json, */*;q=0.5 <br>
Accept-Encoding: gzip, deflate <br>
Connection: keep-alive <br>
Content-Length: 75 <br>
Content-Type: application/json <br>
Host: 127.0.0.1:8000 <br>
User-Agent: HTTPie/2.5.0 <br>

#### BODY
```
{
    "email": "j@naver.com",
    "nickname": "wanted11",
    "password": "aA!@1234567"
}
```

<br>

### response

#### HEADERS

HTTP/1.1 201 Created <br>
Content-Length: 22 <br>
Content-Type: application/json <br>
Date: Tue, 26 Oct 2021 20:37:49 GMT <br>
Referrer-Policy: same-origin <br>
Server: WSGIServer/0.2 CPython/3.8.12 <br>
Vary: Origin <br>
X-Content-Type-Options: nosniff <br>
X-Frame-Options: DENY <br>

#### BODY

```
{
    "message": "SUCCESS"
}
```

<br><br><br>

## POST 로그인 API
http://127.0.0.1:8000/users/login

<br>

### request
POST /users/login HTTP/1.1 <br>
Accept: application/json, */*;q=0.5 <br>
Accept-Encoding: gzip, deflate <br>
Connection: keep-alive <br>
Content-Length: 75 <br>
Content-Type: application/json <br> 
Host: 127.0.0.1:8000 <br>
User-Agent: HTTPie/2.5.0 <br>
```
{ 
  "email": "j@naver.com", 
  "nickname": "wanted11", 
  "password": "aA!@1234567" 
}
```

<br>

### response

HTTP/1.1 201 Created <br>
Content-Length: 113 <br>
Content-Type: application/json <br>
Date: Tue, 26 Oct 2021 20:48:41 GMT <br>
Referrer-Policy: same-origin <br>
Server: WSGIServer/0.2 CPython/3.8.12 <br>
Vary: Origin <br>
X-Content-Type-Options: nosniff <br>
X-Frame-Options: DENY <br>

```
{
   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTF9.xIn-byZ47uY6BQ7Uhpg2m_WRCrabptc8G0xAtYo3350"
}
```

<br><br><br>

## POST 게시판 글 작성 API

http://127.0.0.1:8000/postings

<br>

### request

#### HEADERS

POST /postings HTTP/1.1 <br>
Accept: application/json, */*;q=0.5 <br>
Accept-Encoding: gzip, deflate <br>
Connection: keep-alive <br>
Content-Length: 75 <br>
Content-Type: application/json <br> 
Host: 127.0.0.1:8000 <br>
User-Agent: PostmanRuntime/7.28/4 <br>
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTF9.xIn-byZ47uY6BQ7Uhpg2m_WRCrabptc8G0xAtYo3350

#### BODY

```
{
    "title" : "가입인사11",
    "content" : "안녕하세요11"
}
```


<br>

### response

#### HEADERS

HTTP/1.1 201 Created <br>
Content-Length: 22 <br>
Content-Type: application/json <br>
Date: Tue, 26 Oct 2021 20:48:41 GMT <br>
Referrer-Policy: same-origin <br>
Server: WSGIServer/0.2 CPython/3.8.12 <br>
Vary: Origin <br>
X-Content-Type-Options: nosniff <br>
X-Frame-Options: DENY <br>

#### BODY

```

{
    "message": "CREATED"
}

```

<br><br><br><br><br>

## GET 게시판 하나의 글 보기 API
------
http://127.0.0.1:8000/postings/\<int:posting_id\> <br>
http://127.0.0.1:8000/postings/1
<br>

### request
#### HEADERS

POST /postings HTTP/1.1 <br>
Accept: application/json, */*;q=0.5 <br>
Accept-Encoding: gzip, deflate <br>
Connection: keep-alive <br>
Content-Length: 75 <br>
Content-Type: application/json <br> 
Host: 127.0.0.1:8000 <br>
User-Agent: PostmanRuntime/7.28/4 <br>

<br>

### response

#### HEADERS

HTTP/1.1 201 Created <br>
Content-Length: 22 <br>
Content-Type: application/json <br>
Date: Tue, 26 Oct 2021 20:48:41 GMT <br>
Referrer-Policy: same-origin <br>
Server: WSGIServer/0.2 CPython/3.8.12 <br>
Vary: Origin <br>
X-Content-Type-Options: nosniff <br>
X-Frame-Options: DENY <br>

#### BODY

```
{
    "result": {
        "id": 1,
        "title": "가입 인사 올립니다",
        "content": "안녕하세요",
        "created_at": "2021-10-24T07:17:51.054Z",
        "updated_at": "2021-10-24T07:17:51.054Z"
    }
}

```

<br><br><br><br><br>

## PATCH 게시판 글 수정 API

http://127.0.0.1:8000/postings/\<int:posting_id\> <br>
http://127.0.0.1:8000/postings/28
<br>

### request
#### HEADERS

POST /postings HTTP/1.1 <br>
Accept: application/json, */*;q=0.5 <br>
Accept-Encoding: gzip, deflate <br>
Connection: keep-alive <br>
Content-Length: 75 <br>
Content-Type: application/json <br> 
Host: 127.0.0.1:8000 <br>
User-Agent: PostmanRuntime/7.28/4 <br>
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTF9.xIn-byZ47uY6BQ7Uhpg2m_WRCrabptc8G0xAtYo3350

```
{
    "title" : "hahah11",
    "content" : "웃으면 복이 와요"
}
```

<br>

### response

#### HEADERS

HTTP/1.1 201 Created <br>
Content-Length: 22 <br>
Content-Type: application/json <br>
Date: Tue, 26 Oct 2021 20:48:41 GMT <br>
Referrer-Policy: same-origin <br>
Server: WSGIServer/0.2 CPython/3.8.12 <br>
Vary: Origin <br>
X-Content-Type-Options: nosniff <br>
X-Frame-Options: DENY <br>

#### BODY

```
{
    "message": "UPDATED"
}

```

<br><br><br><br><br>


## DELETE 게시판 글 삭제 API
------
http://127.0.0.1:8000/postings/\<int:posting_id\> <br>
http://127.0.0.1:8000/postings/28

<br>

### request
#### HEADERS

POST /postings HTTP/1.1 <br>
Accept: application/json, */*;q=0.5 <br>
Accept-Encoding: gzip, deflate <br>
Connection: keep-alive <br>
Content-Length: 75 <br>
Content-Type: application/json <br> 
Host: 127.0.0.1:8000 <br>
User-Agent: PostmanRuntime/7.28/4 <br>
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTF9.xIn-byZ47uY6BQ7Uhpg2m_WRCrabptc8G0xAtYo3350

<br>

### response

#### HEADERS

HTTP/1.1 201 Created <br>
Content-Length: 22 <br>
Content-Type: application/json <br>
Date: Tue, 26 Oct 2021 20:48:41 GMT <br>
Referrer-Policy: same-origin <br>
Server: WSGIServer/0.2 CPython/3.8.12 <br>
Vary: Origin <br>
X-Content-Type-Options: nosniff <br>
X-Frame-Options: DENY <br>

#### BODY

```
{
    "message": "DELETED"
}

```
<br><br><br><br><br>

## GET 게시판 글 목록 API
------
http://127.0.0.1:8000/postings/list <br>
http://127.0.0.1:8000/postings/list?page=1

<br>

### request
#### HEADERS

POST /postings HTTP/1.1 <br>
Accept: application/json, */*;q=0.5 <br>
Accept-Encoding: gzip, deflate <br>
Connection: keep-alive <br>
Content-Length: 75 <br>
Content-Type: application/json <br> 
Host: 127.0.0.1:8000 <br>
User-Agent: PostmanRuntime/7.28/4 <br>

<br>

### response

#### HEADERS

HTTP/1.1 201 Created <br>
Content-Length: 22 <br>
Content-Type: application/json <br>
Date: Tue, 26 Oct 2021 20:48:41 GMT <br>
Referrer-Policy: same-origin <br>
Server: WSGIServer/0.2 CPython/3.8.12 <br>
Vary: Origin <br>
X-Content-Type-Options: nosniff <br>
X-Frame-Options: DENY <br>

#### BODY

```
{
    "result": [
        {
            "id": 1,
            "title": "가입 인사 올립니다",
            "created_at": "2021-10-24T07:17:51.054Z"
        },
        {
            "id": 2,
            "title": "가입 인사올립니다2",
            "created_at": "2021-10-24T09:40:11.404Z"
        },
        {
            "id": 3,
            "title": "가입 인사올립니다3",
            "created_at": "2021-10-24T13:31:41.636Z"
        },
        {
            "id": 4,
            "title": "가입 인사올립니다4",
            "created_at": "2021-10-24T13:48:03.966Z"
        },
        {
            "id": 5,
            "title": "가입 인사올립니다5",
            "created_at": "2021-10-24T14:32:44.819Z"
        }
    ]
}

```


