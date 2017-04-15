"""Config validation setup."""
import trafaret as t


CONFIG_TRAFARET = t.Dict({
    t.Key('DEBUG'): t.Bool,
    t.Key('DATABASE_NAME'): t.String,
    t.Key('DATABASE_USERNAME'): t.String,
    t.Key('DATABASE_PASSWORD'): t.String,
    t.Key('DATABASE_HOST'): t.String,
    t.Key('DATABASE_PORT'): t.Int
})
