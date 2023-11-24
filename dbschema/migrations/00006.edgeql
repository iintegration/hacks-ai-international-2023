CREATE MIGRATION m1epry3g4chz74nwawdl27rjbqxvq62z7rx6toxwiwcp4q272lviga
    ONTO m16p3aimzu762zfdo2zqcq5e5jcqto6o4lummvs6xywn7k23gwqrda
{
  ALTER TYPE default::Lecture {
      DROP INDEX fts::index ON (fts::with_options(.text, language := fts::Language.rus));
  };
};
