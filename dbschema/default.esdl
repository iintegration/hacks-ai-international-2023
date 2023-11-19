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
    scalar type LectureStatus extending enum<Created, Processing, Processed>;

    type Lecture extending meta::Times {
        required filename: str;
        required status: LectureStatus {
            default := LectureStatus.Created;
        }

        index fts::index on (
            fts::with_options(
              .filename,
              language := fts::Language.eng
            )
        );
    }
}
