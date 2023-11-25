<template>
  <div class="file-preview">
    <div class="file-preview__title">
      <div v-if="file.status === 'Processed'" class="file-preview__title"  v-ripple @click="setFile">
        {{file.filename}}
      </div>
      <div v-else-if="file.status === 'Error'" class="file-preview__title--error">
        Ошибка {{file.error}}
      </div>
      <div v-else class="file-preview__title--processing">
        {{file.filename}}
        <v-progress-circular indeterminate :size="64"></v-progress-circular>
      </div>
    </div>
    <div class="file-preview__name">
      {{file.filename}}
    </div>
  </div>
</template>

<script>
export default {
  name: "file-preview",
  methods: {
    setFile() {
      this.selectFileId(this.file.id)
      this.moveToFile()
    },
    moveToFile(){
      this.selectMenu('testfileview')
    }
  },
  props: {
    file: {
      type: Object,
    },
    selectMenu: {
    },
    selectFileId: {
    }
  },

}
</script>

<style lang="scss" scoped>
  .file-preview {
    cursor: pointer;
  .file-preview__name {
    width: 355px;
  }
    .file-preview__title {
      height: 200px;
      width: 355px;
      border: solid gray 1px;
      border-radius: 20px;
      display: flex;
      background-color: #8D46F6;
      font-family: "Roboto", sans-serif;
      font-weight: bold;
      font-size: 120%;
      color: #D8D8D8;
      align-items: center;
      justify-content: center;
      .file-preview__title--processing {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #6a6681;
        border-radius: 20px;
        cursor: auto;
        .v-progress-circular {
          position: absolute;
          color: black;
        }
      }
      .file-preview__title--error {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        cursor: auto;
        background: #ff1d5e;
      }
    }
  }
</style>