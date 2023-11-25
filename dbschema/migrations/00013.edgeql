CREATE MIGRATION m17rkhs7lgdpg5uqeu5almeeoynnchg2hn6yd6dep7wuzfeulgun7a
    ONTO m1x2wzmoiyb6rmjbfz6lyde66t7vtyoone6ovf3nurrlbz5xrv7eiq
{
  ALTER TYPE default::Lecture {
      ALTER LINK terms {
          CREATE ANNOTATION std::description := 'Термины лекции';
      };
      ALTER PROPERTY summary {
          CREATE ANNOTATION std::description := 'Конспект лекции';
      };
  };
};
