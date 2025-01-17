# The `duqtools` config file

UQ run settings are configured using a yaml configuration file in the project directory. By default it is named `duqtools.yaml`. You can specify another path for it using the -c/--config option (see `duqtools help` or the [cli](../command-line-interface)).

As a minimum, this configuration file must define the root workspace and the system to use (see below). All other settings are (in principle) optional.


## Starting from scratch

To help initialize a starting config to modify, you can run [`duqtools init`](../command-line-interface#init).

<script id="asciicast-Byj5a5Z9dUI0tEw0q6P7RMnO5" src="https://asciinema.org/a/Byj5a5Z9dUI0tEw0q6P7RMnO5.js" async></script>

Check out the different subpages of this section that explain the different parts of the config.

- [setup](../config/setup)
- [create](../config/create)
- [submit](../config/submit)
- [status](../config/status)
- [system](#defining-the-system)
- [variables](#extra-variables)

### Example config file

Below is an example config file generated by `duqtools init`.

```yaml title="duqtools.yaml"
{!../src/duqtools/data/duqtools.yaml!}
```

## Defining the system

Currently there are multiple systems available. They are distinguished by specifying the `system` field.

Options:

- `jetto` (alias for `jetto-v220922`)
- `jetto-v220922`
- `jetto-v220921`
- `ets6`
- `no-system` (default)

```yaml title="duqtools.yaml"
system:
  name: jetto
```

### Jetto-v220922

::: duqtools.systems.jetto.JettoSystemV220922
    options:
      show_root_toc_entry: false
      members: None
      show_bases: False

### Jetto-v210921

::: duqtools.systems.jetto.JettoSystemV210921
    options:
      show_root_toc_entry: false
      members: None
      show_bases: False

### Ets6

::: duqtools.systems.ets.Ets6System
    options:
      show_root_toc_entry: false
      members: None
      show_bases: False

### No system

::: duqtools.systems.no_system.NoSystem
    options:
      show_root_toc_entry: false
      members: None
      show_bases: False

## Extra variables

Duqtools comes with a list of default [variables](../variables.md). You can update or add your own variables via the `extra_variables` key in the `duqtools.yaml` file.

### IDS variables

{{ schema_IDSVariableModel['description'] }}

{% for name, prop in schema_IDSVariableModel['properties'].items() %}
`{{ name }}`
: {{ prop['description'] }}
{% endfor %}

Example:

```yaml title="duqtools.yaml"
extra_variables:
- name: rho_tor_norm
  ids: core_profiles
  path: profiles_1d/*/grid/rho_tor_norm
  dims: [time, x]
  type: IDS-variable
- name: t_i_ave
  ids: core_profiles
  path: profiles_1d/*/t_i_ave
  dims: [time, x]
  type: IDS-variable
```

### Jetto variables

{{ schema_JettoVariableModel['description'] }}

{% for name, prop in schema_JettoVariableModel['properties'].items() %}
`{{ name }}`
: {{ prop['description'] }}
{% endfor %}

The lookup key is defined by a so-called *jetto variable*, which maps to one or more locations in the jetto system configs (e.g., `jetto.jset`, or `jetti.in`).

{{ schema_JettoVar['description'] }}

{% for name, prop in schema_JettoVar['properties'].items() %}
`{{ name }}`
: {{ prop['description'] }}
{% endfor %}

The exact fields to write to are defined under the `keys` section, which takes the `file` to write to, the `section` (if applicable) and `field` the variable is mapped to.

Example:

```yaml title="duqtools.yaml"
extra_variables:
- name: major_radius
  type: jetto-variable
  lookup:
    name: major_radius
    doc: Reference major radius (R0)
    type: float
    keys:
    - field: EquilEscoRefPanel.refMajorRadius
      file: jetto.jset
    - field: RMJ
      file: jetto.in
      section: NLIST1
```

### Top level

These are the top level keywords in the config. See the specific sections for more information.

{% for name, prop in schema_ConfigModel['properties'].items() %}
`{{ name }}`
: {{ prop['description'] }}
{% endfor %}
