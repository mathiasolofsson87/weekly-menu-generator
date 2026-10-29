# Dashboard and automation examples

Entity ids below are the ones created with Home Assistant in English. If yours differ (for example because Home Assistant was in Swedish when the integration was added), find them under *Settings → Devices & services → Weekly Menu Generator*.

## The custom cards

They are added to your dashboards automatically and need no entity configuration.

```yaml
type: custom:weeklymenu-menu-card
title: Dinners this week
show_images: true
show_actions: true
```

```yaml
type: custom:weeklymenu-today-card
show_image: true
show_ingredients: false
```

```yaml
type: custom:weeklymenu-shopping-card
show_added: true
show_skipped: false
```

```yaml
type: custom:weeklymenu-family-card
editable: true
```

## Stock cards

Tonight's dinner as a tile:

```yaml
type: tile
entity: sensor.weekly_menu_generator_today_s_dinner
name: Tonight's dinner
icon: mdi:silverware-fork-knife
```

The week as a list:

```yaml
type: entities
title: This week
entities:
  - sensor.weekly_menu_generator_monday
  - sensor.weekly_menu_generator_tuesday
  - sensor.weekly_menu_generator_wednesday
  - sensor.weekly_menu_generator_thursday
  - sensor.weekly_menu_generator_friday
```

A calendar of the planned dinners, and buttons for the two things you do each week:

```yaml
type: calendar
entities:
  - calendar.weekly_menu_generator_dinner_menu
---
type: horizontal-stack
cards:
  - type: button
    entity: button.weekly_menu_generator_generate_menu
    name: New menu
  - type: button
    entity: button.weekly_menu_generator_confirm_menu
    name: Confirm
```

Today's ingredients and who gets a different version, as Markdown:

```yaml
type: markdown
title: "{{ states('sensor.weekly_menu_generator_today_s_dinner') }}"
content: >
  {% set d = states.sensor.weekly_menu_generator_today_s_dinner.attributes %}
  {% for line in d.ingredients | default([]) %}
  - {{ line }}
  {% endfor %}
  {% for g in (d.split.groups if d.split else []) %}
  **{{ g.members | join(', ') }}:** {% for s in g.substitutions %}{{ s.original.raw }} → {{ s.replacement.raw }}{% endfor %}
  {% endfor %}
```

## Automations

Tell the family what's for dinner:

```yaml
alias: Announce dinner
triggers:
  - trigger: time
    at: "16:30:00"
conditions:
  - condition: template
    value_template: "{{ states('sensor.weekly_menu_generator_today_s_dinner') not in ['unknown', 'unavailable'] }}"
actions:
  - action: notify.mobile_app_your_phone
    data:
      title: Dinner tonight
      message: "{{ states('sensor.weekly_menu_generator_today_s_dinner') }}"
```

Confirm automatically on Saturday evening if nobody did:

```yaml
alias: Confirm the menu on Saturday evening
triggers:
  - trigger: time
    at: "18:00:00"
conditions:
  - condition: time
    weekday: [sat]
  - condition: state
    entity_id: sensor.weekly_menu_generator_status
    state: draft
actions:
  - action: weeklymenu.confirm_menu
```

React when the menu is ready or confirmed (the events carry the week, and any warnings or shopping counts):

```yaml
triggers:
  - trigger: event
    event_type: weeklymenu_menu_ready
  # or: weeklymenu_confirmed
```

Add a guest to the family for a week, or change a preference, with `weeklymenu.set_member`:

```yaml
action: weeklymenu.set_member
data:
  name: Anna
  diet: vegetarian
  attends: [mon, tue, wed, thu]
```
