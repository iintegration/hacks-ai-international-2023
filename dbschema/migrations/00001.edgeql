CREATE MIGRATION m1nztmfjaycbxebhvbh4em25fjsamodccldaqfjjryqla7ygyqqgra
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
      CREATE REQUIRED PROPERTY filename: std::str;
      CREATE INDEX fts::index ON (fts::with_options(.filename, language := fts::Language.eng));
  };
  CREATE SCALAR TYPE default::LectureStatus EXTENDING enum<Created, Processing, Processed>;
  CREATE TYPE default::Lecture EXTENDING meta::Times {
      CREATE LINK file: default::File {
          ON SOURCE DELETE DELETE TARGET;
      };
      CREATE REQUIRED PROPERTY status: default::LectureStatus {
          SET default := (default::LectureStatus.Created);
      };
  };
  ALTER TYPE default::File {
      CREATE LINK lecture := (.<file[IS default::Lecture]);
  };
};
