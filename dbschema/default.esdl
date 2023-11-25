module meta {
  abstract type Created {
    created: datetime {
      rewrite insert using (datetime_of_statement())
    }
  }

  abstract type Modified {
    modified: datetime {
      rewrite update using (datetime_of_statement())
    }
  }

  abstract type Times extending meta::Created, meta::Modified;
}

module default {
    scalar type LectureStatus extending enum<Created, Processing, Processed, Error>;

    type File extending meta::Times {
        required filename: str {
            annotation description := 'Название файла пользователя';
        }
        required filename_suffix: str {
            annotation description := 'Расширение файла пользователя';
        }
        object_name := <str>(.id) ++ .filename_suffix;
        link lecture := .<file[is Lecture];

        index fts::index on (
            fts::with_options(
              .filename,
              language := fts::Language.eng
            )
        );
    }

    type Term extending meta::Times {
        required term: str;
        required definition: str;
        required start_timestamp: float32;
        required end_timestamp: float32;
    }

    type Lecture extending meta::Times {
        required status: LectureStatus {
            default := LectureStatus.Created;
        }
        link file: File {
            on source delete delete target;
        }
        text: str {
            annotation description := 'Полный текст лекции';
        }
        timestamps: json;
        summary: str {
            annotation description := 'Конспект лекции';
        }
        multi link terms: Term {
            annotation description := 'Термины лекции';
        }
        error: str {
            annotation description := 'Ошибка, которая возникла во время обработки моделями';
        }
    }
}
