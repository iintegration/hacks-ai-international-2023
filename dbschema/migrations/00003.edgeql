CREATE MIGRATION m1nhrzqg2sk62dabn76r5npqeruhxnc36qvtyq2k2gk2b6txcr2kca
    ONTO m1jkvzm7ag3mg64ilc5iwsln6yndan7ujsjd6jbcsv5viifgok27mq
{
  ALTER TYPE default::Analysis {
      DROP INDEX fts::index ON (fts::with_options(.text, language := fts::Language.rus));
      DROP LINK lecture;
      DROP PROPERTY text;
  };
  ALTER TYPE default::Lecture {
      DROP LINK analysis;
  };
  DROP TYPE default::Analysis;
  ALTER TYPE default::Lecture {
      CREATE PROPERTY text: std::str;
      CREATE INDEX fts::index ON (fts::with_options(.text, language := fts::Language.rus));
  };
  CREATE SCALAR TYPE default::AnalysisStatus EXTENDING enum<Success, Error>;
};
