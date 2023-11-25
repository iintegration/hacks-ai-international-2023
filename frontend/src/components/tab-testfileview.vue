
<template>
  <div v-if="error">
    <v-overlay v-model="error" @click="this.error = false;
  selectFileId('');
  selectMenu('base')">
      <v-card>
        <h1>
          Произошла какая то ошибка, возможно сервер не отвечает, попробуйте позже
        </h1>
        <v-card-actions>
          <v-btn @click="this.error = false;  selectFileId('');
  selectMenu('base')">
            Закрыть
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-overlay>
  </div>
  <div v-else class="tab-fileview">
    <div class="tab-fileview__back-button">
      <div class="tab-fileview__back-button__button" @click="backToBase">
        Вернуться назад
      </div>
      <div class="tab-fileview__back-button__lection-text">
        Лекция: {{testData.filename}}
      </div>
    </div>

    <div class="tab-fileview__uppper-section">
      <div class="uppper-section__video">
<!--        <audio-player :src="'https://minio-api.sosus.org/bucket/ed942690-8ace-11ee-a5ad-0fe3df294a75?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=XGLZ1YURKZXK37I07I6J%2F20231124%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231124T175533Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJYR0xaMVlVUktaWEszN0kwN0k2SiIsImV4cCI6MTcwMDg3NDg2MiwicGFyZW50IjoiOTg3ZDRmMDg5NWZlMzA0YWFiNTNkMDNjIn0.Vk2KhPWIwmkgv5ELfO426d1QfDynNVh2OXUrh7LqnhP9pwGwmiIBIiBAxyFhzDnbpSDFw-J4VbKkD6aKfY3y0A&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=73ec203c6933c4bf48f862c34723fb41cf922583ff3b9b630996984499022284'">
        </audio-player>-->
        <audio-player :option="{
          src: testData.download_link,
          coverImage: require('@/assets/logoWhite.svg')
        }">
        </audio-player>
      </div>
      <div class="uppper-section__transcr" >
        <div class="uppper-section__transcr__element" v-for="i in testData.timestamps" :key="i">
          <time-stamp-text-test :file-text="i" :gloss="testData.terms" :selected-termi="selectedTermin">

          </time-stamp-text-test>
        </div>
      </div>
    </div>
    <div class="tab-fileview__down-section">
      <div class="down-section__glos">
        <div v-if="testData.terms != ''">
          <div v-for="i in testData.terms" :key="i">
            <gloss-component
                :oneGloss="i"
                :hightlight-termin="hightlightTermin"
                :deleteGlossTerm="deleteGlossTerm"
                :selected-termi="selectedTermin">
            </gloss-component>
          </div>
        </div>
        <div v-else style="display: flex; justify-content: center">
          Глоассарий не загружен
        </div>

        <div class="down-section__glos__add-button" v-if="testData.terms">
          <img :src="require('@/assets/Download_ico.png')" height="40" width="40" style="cursor:pointer;" @click="download" >
        </div>
      </div>
      <div class="down-section__consp">
        <div v-if="testData.summary" style="display: flex; flex-direction: column ">
          {{testData.summary}}
          <div style="display: flex; flex-direction: column; align-items: center">
            <img :src="require('@/assets/Download_ico.png')" height="40" width="40" style="cursor:pointer;" @click="download1" >
          </div>

        </div>
        <div v-else style="display: flex; justify-content: center">
          Конспектр не загружен
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import AudioPlayer from 'vue3-audio-player'
import 'vue3-audio-player/dist/style.css'
import TimeStampTextTest from "@/components/time-stamp-text-test";
import timeTestStamp from "@/assets/testData.json";
import textTrans from "@/components/text-trans";
//import { AudioPlayer, VideoPlayer } from 'vue-md-player'
import gloss from "@/assets/gloss.json"
import text from "@/assets/text.json"
import glossComponent from "@/components/gloss-component";
import FrontConf from "/src/Front.json";

export default {
  name: "tab-testfileview",
  computed: {
  },
  data() {
    return {
      testData: '',
      error: false,
      gloss: gloss,
      text: text,
      selectedTermin: ''
    }
  },
  props: {
    selectMenu: {
    },
    selectFileId: {
    },
    fileId: {
    },
    selectedMenu: {
    },

  },

  methods: {
    deleteGlossTerm(termin) {
      for (let i in this.testData.terms) {
        if (this.testData.terms[i].term == termin) {
          console.log(this.testData.terms[i])
          this.testData.terms.splice(i,1)
          console.log(this.testData.terms[i])
        }
      }
    },
    download() {
      let text = JSON.stringify(this.testData.terms);
      let filename = 'export.json';
      let element = document.createElement('a');
      element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(text));
      element.setAttribute('download', filename);

      element.style.display = 'none';
      document.body.appendChild(element);

      element.click();
      document.body.removeChild(element);
  },
    download1() {
      let text = JSON.stringify(this.testData.summary);
      let filename = 'conspect.txt';
      let element = document.createElement('a');
      element.setAttribute('href', 'data:application/txt;charset=utf-8,' + encodeURIComponent(text));
      element.setAttribute('download', filename);

      element.style.display = 'none';
      document.body.appendChild(element);

      element.click();
      document.body.removeChild(element);
    },
    backToBase() {
      this.selectFileId('')
      this.selectMenu('Base')
    },
    hightlightTermin(termin) {
      this.selectedTermin = termin
      console.log('Термин = ', termin)
    }
  },
  components: {
    TimeStampTextTest,
    AudioPlayer,
    textTrans,
    glossComponent,
  },
  beforeCreate() {
    console.log(this.fileId)
    axios.get(`${FrontConf.domain}v1/lectures/${this.fileId}/`).then(
        response => {
         this.testData = response.data
          console.log('Загрузилось', response.data)

        })
        .catch(reason => {
          console.log('Ошибка загрузки')
          this.error = true
        })
  }
}
</script>

<style lang="scss" scoped>
  .tab-fileview {
    padding: 1vh 2vw;
    width: 100%;
    min-width: 90vw;
    .tab-fileview__uppper-section{
      display: flex;
      justify-content: space-around;
      gap: 10px;
      margin-top: 1vh;
      .uppper-section__video {
        height: 500px;
        width: 800px;
        border: #D8D8D8 solid;
        border-radius: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        .audio__player{
          width: 80%;
        }
      }
      .uppper-section__transcr {
        padding: 10px;
        border: #D8D8D8 solid;
        border-radius: 20px;
        width: 100%;
        display: flex;
        flex-direction: row;
        overflow-y:scroll;
        flex-wrap: wrap;
        max-height: 500px;
        justify-content: left;
        align-content: flex-start;
        .uppper-section__transcr__element{
          display: flex;
          align-content: flex-start;
          flex-direction: row;
        }
        .uppper-section__transcr__title {
          border-bottom: #6a6681 solid;
          display: flex;
          gap: 20px;
          margin-bottom: 20px;
          align-items: center;
          .transcr__title__timestamp {
            border-right: #6a6681 solid;
            padding: 5px 1px 5px 1px;
          }
        }
      }
    }
    .tab-fileview__down-section {
      margin-top: 2vh;
      display: flex;
      justify-content: space-around;
      gap: 10px;
      .down-section__glos {
        border: #D8D8D8 solid;
        border-radius: 20px;
        width: 800px;
        height: 500px;
        padding: 10px;
        overflow-y: scroll;
        .down-section__glos__add-button {
          display: flex;
          align-items: center;
          justify-content: center;
        }
      }
      .down-section__consp {
        height: 500px;
        border: #D8D8D8 solid;
        border-radius: 20px;
        width: 800px;
        padding: 10px;
        overflow: scroll;
      }
    }
    .tab-fileview__back-button{
      display: flex;
      justify-content: space-between;
    }
    .tab-fileview__back-button__lection-text {
      margin-left: 10px;
      font-style: normal;
      cursor: default;
      color: gray;
      width: 100%;
      text-align: end;
      text-overflow: ellipsis;

    }
    .tab-fileview__back-button__button {
      color: gray;
      font-style: italic;
      cursor: pointer;
      width: 100%;
    }
  }
</style>