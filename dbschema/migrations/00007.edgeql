CREATE MIGRATION m1tbsrf7wtufkb3f3q3ihjuidyaedm6ta6u34n7rpvhfeluclt4xsa
    ONTO m1epry3g4chz74nwawdl27rjbqxvq62z7rx6toxwiwcp4q272lviga
{
  ALTER TYPE default::File {
      ALTER PROPERTY filename {
          CREATE ANNOTATION std::description := 'Название файла пользователя';
      };
  };
  ALTER TYPE default::Lecture {
      ALTER PROPERTY error {
          CREATE ANNOTATION std::description := 'Ошибка, которая возникла во время обработки моделями';
      };
      ALTER PROPERTY text {
          CREATE ANNOTATION std::description := 'Полный текст лекции';
      };
  };
};
