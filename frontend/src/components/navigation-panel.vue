<template>
  <div class="nav-panel">
    <div class="nav-panel--overlay" @click="this.$emit('toggleMenu')"></div>
    <div class="nav-panel__body">
      <div class="nav-panel__buttons">
        <div :class="[isLection ? 'buttons__button--selected' : 'buttons__button']" @click="selectMenu('Lections')">
          Ввод лекций
        </div>
        <div :class="[isBase ? 'buttons__button--selected' : 'buttons__button']" @click="selectMenu('Base')">
          База лекций
        </div>
        <div :class="[isSettings ? 'buttons__button--selected' : 'buttons__button']" @click="selectMenu('Settings')">
          Настройки
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "navigation-panel",
  props: {
    menuOpened: {
      type: Boolean,
      default: false
    },
    selectedButton: {
      type: String,
    },
    selectMenu: {},
    fileId: {
      type: String
    }
  },
  computed: {
    isLection() {
      if (this.selectedButton == 'Lections') {
        return true
      } else return false
    },
    isBase() {
      if (this.selectedButton == 'Base') {
        return true
      } else return false
    },
    isSettings() {
      if (this.selectedButton == 'Settings') {
        return true
      } else return false
    }
  },
  methods: {},
}
</script>

<style lang="scss" scoped>
.nav-panel--overlay {
  background: rgba(0, 0, 0, 0.2);
  height: 100%;
  width: 80%;
}
.nav-panel {
  position: fixed;
  display: flex;
  height: 100vh;
  width: 100%;
  z-index: 10;
  flex-direction: row-reverse;
}
.nav-panel__body {
  padding: 0 0 0 20px;
  border-right: solid 1px #D8D8D8;
  width: 20vw;
  height: 100%;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;

  .nav-panel__buttons {
    cursor: pointer;
    gap: 10px;
    display: flex;
    flex-direction: column;
    font-size: 3vh;

    .buttons__button {
      color: #9C9FB0;
    }

    .buttons__button--selected {
      color: #8D46F6;
    }
  }
}
</style>