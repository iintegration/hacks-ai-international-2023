CREATE MIGRATION m1x2wzmoiyb6rmjbfz6lyde66t7vtyoone6ovf3nurrlbz5xrv7eiq
    ONTO m1zohfexkh2tg6btlyxc224hhebjizdbsdung6zrdl7kl2l3ryt52a
{
  ALTER TYPE default::Lecture {
      CREATE PROPERTY summary: std::str;
  };
};
