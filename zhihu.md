# API文档


| API | 功能 |
|--------|--------|
|API.user_timeline()|查看用户近期状态|
|API.hide_question()|隐藏问题|
|API.display_question()|显示问题|

##API.user_timeline()

####支持格式

json

####请求参数

| 参数 | 必选 | 类型及范围 | 说明 |
|--------|--------|--------|--------|
| user_id | true | string | 需要查询用户的ID |
| page | false | int | 分页请求,页数,默认为0 |
| length | false | int | 分页请求,分页长度,默认为-1 |

####返回结果

```json
[
  {
    "action": "3",
    "unix_time": 5751557923,
    "question_id": "7341"
  },
  {
    "action": "5",
    "unix_time": 5701735163,
    "question_id": "3625"
  },
  ...
]
```

####返回字段说明

| 参数 | 类型及范围 | 说明 |
|--------|--------|--------|
| action | string | 用户动作,1:提问,2:回答,3:赞同,4:关注问题,5:关注话题,6:关注用户,7:发表文章 |
| unix_time | int | 动作发生的unix时间 |
| question_id | string | 问题ID |

####注意事项

1. 默认起始页为```0```
2. 如果输入参数page,length为空,将默认返回用户全部的活动信息

##API.hide_question()

####支持格式

json

####请求参数

| 参数 | 必选 | 类型及范围 | 说明 |
|--------|--------|--------|--------|
| user_id | true | string | 用户ID |
| question_id | true | string | 需要隐藏的问题ID |

####返回结果

成功

```json
{"r": "1"}
```

失败

```json
{"r": "0"}
```

##API.display_question()

####支持格式

json

####请求参数

| 参数 | 必选 | 类型及范围 | 说明 |
|--------|--------|--------|--------|
| user_id | true | string | 用户ID |
| question_id | true | string | 需要显示的问题ID |

####返回结果

成功

```json
{"r": "1"}
```

失败

```json
{"r": "0"}
```
