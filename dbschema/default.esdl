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

    type File extending meta::Times {
        required filename: str;
        link lecture := .<file[is Lecture];

        index fts::index on (
            fts::with_options(
              .filename,
              language := fts::Language.eng
            )
        );
    }

    type Lecture extending meta::Times {
        required status: LectureStatus {
            default := LectureStatus.Created;
        }
        link file: File;
    }
}
