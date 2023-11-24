CREATE MIGRATION m16p3aimzu762zfdo2zqcq5e5jcqto6o4lummvs6xywn7k23gwqrda
    ONTO m16klaliflbk7yvd7pr5peh4m75o5ydkqpnf3lsj5kg3gfttesytta
{
  ALTER TYPE default::Lecture {
      CREATE PROPERTY error: std::str;
  };
  ALTER SCALAR TYPE default::LectureStatus EXTENDING enum<Created, Processing, Processed, Error>;
};
