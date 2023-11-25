CREATE MIGRATION m1gkynuygnkacuaabcxi64p6f2wapp4bcaindzvyrfxe6h4ivox5ka
    ONTO initial
{
  CREATE MODULE meta IF NOT EXISTS;
  CREATE ABSTRACT TYPE meta::Created {
      CREATE PROPERTY created: std::datetime {
          CREATE REWRITE
              INSERT 
              USING (std::datetime_of_statement());
      };
  };
  CREATE ABSTRACT TYPE meta::Modified {
      CREATE PROPERTY modified: std::datetime {
          CREATE REWRITE
              UPDATE 
              USING (std::datetime_of_statement());
      };
  };
  CREATE ABSTRACT TYPE meta::Times EXTENDING meta::Created, meta::Modified;
  CREATE TYPE default::File EXTENDING meta::Times {
      CREATE REQUIRED PROPERTY filename: std::str {
          CREATE ANNOTATION std::description := 'Название файла пользователя';
      };
      CREATE INDEX fts::index ON (fts::with_options(.filename, language := fts::Language.eng));
      CREATE REQUIRED PROPERTY filename_suffix: std::str {
          CREATE ANNOTATION std::description := 'Расширение файла пользователя';
      };
      CREATE PROPERTY object_name := ((<std::str>.id ++ .filename_suffix));
  };
  CREATE TYPE default::Term EXTENDING meta::Times {
      CREATE REQUIRED PROPERTY definition: std::str;
      CREATE REQUIRED PROPERTY end_timestamp: std::float32;
      CREATE REQUIRED PROPERTY start_timestamp: std::float32;
      CREATE REQUIRED PROPERTY term: std::str;
  };
  CREATE SCALAR TYPE default::LectureStatus EXTENDING enum<Created, Processing, Processed, Error>;
  CREATE TYPE default::Lecture EXTENDING meta::Times {
      CREATE LINK file: default::File {
          ON SOURCE DELETE DELETE TARGET;
      };
      CREATE MULTI LINK terms: default::Term {
          CREATE ANNOTATION std::description := 'Термины лекции';
      };
      CREATE PROPERTY error: std::str {
          CREATE ANNOTATION std::description := 'Ошибка, которая возникла во время обработки моделями';
      };
      CREATE REQUIRED PROPERTY status: default::LectureStatus {
          SET default := (default::LectureStatus.Created);
      };
      CREATE PROPERTY summary: std::str {
          CREATE ANNOTATION std::description := 'Конспект лекции';
      };
      CREATE PROPERTY text: std::str {
          CREATE ANNOTATION std::description := 'Полный текст лекции';
      };
      CREATE PROPERTY timestamps: std::json;
  };
  ALTER TYPE default::File {
      CREATE LINK lecture := (.<file[IS default::Lecture]);
  };
};
