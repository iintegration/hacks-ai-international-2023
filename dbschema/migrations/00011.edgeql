CREATE MIGRATION m1zohfexkh2tg6btlyxc224hhebjizdbsdung6zrdl7kl2l3ryt52a
    ONTO m1mhde2r5vzvr4i4qk3nu4mjdwgklwo3qv7yyf2tcmevsokwaahicq
{
  CREATE TYPE default::Term EXTENDING meta::Times {
      CREATE REQUIRED PROPERTY definition: std::str;
      CREATE REQUIRED PROPERTY end_timestamp: std::float32;
      CREATE REQUIRED PROPERTY start_timestamp: std::float32;
      CREATE REQUIRED PROPERTY term: std::str;
  };
  ALTER TYPE default::Lecture {
      CREATE MULTI LINK terms: default::Term;
  };
};
