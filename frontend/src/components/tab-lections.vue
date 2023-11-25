<template>
  <div v-if="isLoading">
    <div v-if="error">
      <v-overlay v-model="error" @click="this.error = false;
              this.isLoading = false; this.$refs.file.value=null;">
        <v-card>
          <h1>
            Произошла какая то ошибка, возможно сервер не отвечает, попробуйте позже
          </h1>
          <v-card-actions>
            <v-btn @click="this.error = false;
              this.isLoading = false; this.$refs.file.value=null;">
              Закрыть
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-overlay>
    </div>
    <div v-else>
      <div class="loading-overlay">
        <div class="circles-to-rhombuses-spinner">
          <div class="circle"></div>
          <div class="circle"></div>
          <div class="circle"></div>
        </div>
      </div>
    </div>
  </div>

  <div class="tab-lections"
       @drop="dragDrop">
    <div class="tab-lections__file-upload"
         @dragover="onDragOver"
         @dragleave="onDragLeave">
      <div class="file-upload">
        <div v-if="isDrag">
          Бросьте файл сюда
        </div>
        <div v-else>
         Для загрузки перетащите файл внутрь пунктирной рамки
          <div>
            Или
          </div>
          <label class="file-upload__upload-button">
            Загрузите файл
            <input type="file" ref="file" @change="initFileButtonLoad">
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios'
import FrontConf from '../Front.json'
async function postLecture(fileName) {
  console.log(fileName)
  return await axios.post(
      `${FrontConf.domain}v1/lectures/`,
      {
        'filename': fileName
      },
      {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }
  )
}
export default {
  name: "tab-lections",
  data() {
    return {
      isDrag: false,
      myFile: '',
      isLoading: false,
      fileUUID: '',
      error: false
    }
  },
  props: {
    selectMenu: {},
  },
  methods: {
    dragDrop(e) {
      e.preventDefault();
      this.initFileDropLoad(e)
    },
    onDragOver(e) {
      e.preventDefault()
      this.isDrag = true
    },
    onDragLeave(e) {
      e.preventDefault()
      this.isDrag = false
    },
    setLoadingFalse() {
      this.isLoading = false
    },
    initFileDropLoad(e){
      this.isDrag = false;
      this.isLoading = true
      this.myFile = e.dataTransfer.files
      console.log(this.myFile)
      postLecture(this.myFile[0].name).then(response => {
        console.log('Лекция есть' + response.data)
        this.loadFile(response.data)
      })
    },
    initFileButtonLoad(){
      this.isDrag = false;
      this.isLoading = true
      this.onChange()
      console.log(this.myFile)
      postLecture(this.myFile[0].name).then(response => {
        console.log('Лекция есть', response.data)
        //this.error = true
        this.loadFile(response.data)
      }).catch(reason => {this.error = true
      console.log('Ошибка старта')})
    },
    onChange(){
      this.myFile = this.$refs.file.files
    },
    loadFile(fileData){
      //let data = new FormData()
      //data.append("file", this.myFile[0])
      console.log(this.myFile[0])
      fetch(fileData.upload_url, {method: 'PUT', body:this.myFile[0]})
          .then(response => {
            console.log('Получилось')
            this.startAnalyze(fileData)
          })
          .catch(reason => {this.error = true
            console.log('Ошибка загрузки', reason)})

    },
    startAnalyze(fileData) {
      axios.post(`${FrontConf.domain}v1/lectures/${fileData.id}/start_analyze/`)
          .then(response => {
            console.log('анализ')
            this.setLoadingFalse()
            this.switchToBase()
          })
          .catch(reason => {this.error = true
            console.log('Ошибка анализа')})
    },
    switchToBase() {
      this.selectMenu('Base')
    }

  },


}
</script>

<style lang="scss" scoped>
.v-overlay {
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
  .v-card {
    padding: 20px;
  }
}
.tab-lections {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 300px;
  .tab-lections__file-upload {
    border: dotted gray 1px;
    border-radius: 20px;
    height: 40vh;
    width: 50vh;
    min-height: 300px;
    min-width: 500px;
    .file-upload {
      gap: 10px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100%;
      text-align: center;
      .file-upload__upload-button {
        border: 1px solid #ccc;
        display: inline-block;
        padding: 6px 12px;
        cursor: pointer;
        color: white;
        border-radius: 20px;
        background-color: #8D46F6;
        input[type="file"] {
          display: none;
        }
      }
      .file-upload__upload-button:hover {
        background-color: #6404ff;
      }
    }
  }
}
.circles-to-rhombuses-spinner, .circles-to-rhombuses-spinner * {
  box-sizing: border-box;
}
.loading-overlay {
  height: 100vh;
  width: 100vw;
  background: rgba(0, 0, 0, 0.8);
  position: fixed;
  top: 0;
  left: 0;
}
.circles-to-rhombuses-spinner {
  height: 100vh;
  width: calc( (15px + 15px * 1.125) * 3);
  top: 50vh;
  left: 48vw;
  display: flex;
  position: fixed;

}

.circles-to-rhombuses-spinner .circle {
  height: 15px;
  width: 15px;
  margin-left: calc(15px * 1.125);
  transform: rotate(45deg);
  border-radius: 10%;
  border: 3px solid #ff1d5e;
  overflow: hidden;
  background: transparent;

  animation: circles-to-rhombuses-animation 1200ms linear infinite;
}

.circles-to-rhombuses-spinner .circle:nth-child(1) {
  animation-delay: calc(150ms * 1);
  margin-left: 0
}

.circles-to-rhombuses-spinner .circle:nth-child(2) {
  animation-delay: calc(150ms * 2);
}

.circles-to-rhombuses-spinner .circle:nth-child(3) {
  animation-delay: calc(150ms * 3);
}

@keyframes circles-to-rhombuses-animation {
  0% {
    border-radius: 10%;
  }

  17.5% {
    border-radius: 10%;
  }

  50% {
    border-radius: 100%;
  }


  93.5% {
    border-radius: 10%;
  }

  100% {
    border-radius: 10%;
  }
}

@keyframes circles-to-rhombuses-background-animation {
  50% {
    opacity: 0.4;
  }
}
</style>