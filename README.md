# easytopics



## Database
sqlite with schema

```dbml
// Docs: https://dbml.dbdiagram.io/docs

Table Documents {
  id integer [primary key]
  doc text
}

Table Topics {
  id integer [primary key]
  external_id integer
  topic_representation text
}

Table Questions {
  id integer [primary key]
  question text
}

Table Answers {
  id integer [primary key]
  doc_id integer
  question_id integer
  answer text
  topic_id integer
}

Ref: Answers.doc_id > Documents.id
Ref: Answers.question_id > Questions.id
Ref: Answers.topic_id > Topics.id
```