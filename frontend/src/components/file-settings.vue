<template>
  <div class="file-settings">
    <div class="file-settings__menu">
      <v-dialog width="500" class="menu__dialog">
        <template v-slot:activator="{ props }" >
          <div  class="menu__dialog__activator-button">
            <button v-ripple variant="tonal" v-bind="props" color="red" text="Удалить все лекции"> Удалить все лекции</button>
          </div>

        </template>
        <template v-slot:default="{ isActive }">
          <v-card title="Dialog">
            <v-card-text>
              Вы уверены что хотите стереть все данные ?
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn class="menu__dialog__delete-button"
                  text="Удалить"
                  @click="deleteAll().then(response => {
                    console.log()
                    isActive.value = false
                  })"
                     color="red"
              ></v-btn>
            </v-card-actions>
          </v-card>
        </template>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import FrontConf from '/src/Front.json'
export default {

  name: "file-settings",
  methods: {
    deleteAll()
    {
      return axios.delete(`${FrontConf.domain}v1/lectures/`)
    }
  },
}
</script>

<style lang="scss" scoped>
.file-settings {
  display: flex;
  padding-left: 10px;
  padding-top: 2vh;
  width: 100%;
  justify-content: center;

  button {
    border: solid #ff1d5e 1px;
    border-radius: 20px;
    padding: 20px;
    color: black;
  }
  button:hover{
    color: white;
    background: #ff1d5e;
    border: solid #ff1d5e 1px;
  }

  .file-settings__menu {
    .menu__dialog {
      .menu__dialog__activator-button{

      }

    }
  }
}
</style>