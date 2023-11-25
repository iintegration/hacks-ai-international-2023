<template>
  <div class="time-stamp-text">
    <div class="time-stamp-text__text">
        <v-tooltip :text="fileText.timestamp[0].toString() + ' - ' + fileText.timestamp[1].toString()">
          <template v-slot:activator="{ props }">
            <div class="time-stamp-text__text--mod" v-bind="props">{{ fileText.text }}</div>
          </template>
        </v-tooltip>
    </div>
  </div>
</template>

<script>

export default {
  name: "time-stamp-text",
  props: {
    fileText: {
      type: Object,
    },
  },
}
</script>

<style lang="scss" scoped>
.time-stamp-text{
  text-align: left;
  display: flex;
  justify-content: left;
  .time-stamp-text__stamp-start{
    .v-chip {
      font-size: 12px;
      width: 80px;
      display: flex;
      justify-content: center;
      position: relative;
    }

  }
  .time-stamp-text__text {
    display: flex;
    margin-left: 0.5em;
    .time-stamp-text__text--mod {
      display: flex;
      justify-content: left;
      align-items: flex-start;
    }
  }
  .time-stamp-text__stamp-end {

  }

}
</style>