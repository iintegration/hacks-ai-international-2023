CREATE MIGRATION m1jkvzm7ag3mg64ilc5iwsln6yndan7ujsjd6jbcsv5viifgok27mq
    ONTO m1nztmfjaycbxebhvbh4em25fjsamodccldaqfjjryqla7ygyqqgra
{
  CREATE TYPE default::Analysis EXTENDING meta::Times {
      CREATE REQUIRED PROPERTY text: std::str;
      CREATE INDEX fts::index ON (fts::with_options(.text, language := fts::Language.rus));
  };
  ALTER TYPE default::Lecture {
      CREATE LINK analysis: default::Analysis {
          ON SOURCE DELETE DELETE TARGET;
      };
  };
  ALTER TYPE default::Analysis {
      CREATE LINK lecture := (.<analysis[IS default::Lecture]);
  };
};
