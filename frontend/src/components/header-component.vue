<template>
  <div class="header">
    <div class="header__body">
      <div class="body__left-side">
        <div class="left-side__menu-button" @click="this.$emit('toggleMenu')">
          <img :src="require('@/assets/burger-button-opened.svg')" v-if="menuOpened">
          <img :src="require('@/assets/burger-buton.svg')" v-else class="left-side__menu-button--opened">
        </div>
        <div class="left-side__logo">
          <img :src="require('@/assets/GeekBrainsLogo.svg')">
        </div>
      </div>
      <div class="body__right-side">
        <div class="right-side__help-ico">
          <v-tooltip :text="hintText">
            <template v-slot:activator="{ props }" >
              <div class="time-stamp-text__text--mod" v-bind="props"> <img :src="require('@/assets/help-ico.svg')" alt="11"></div>
            </template>
          </v-tooltip>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "header-component",
  data() {
    return {
    }
  },
  props: {
    menuOpened: {
      type: Boolean,
      default: false
    },
    selectedMenuItem() {
      return String;
    }
  },
  computed: {
    hintText() {
      let text = ''
      if (this.selectedMenuItem == 'Base') {
        text = 'Это вкладка со всеми загруженными вами лекциями. ' +
            'Тут появляются лекции которые вы загрузили. ' +
            'Если вы видите серую рамку и вращающийся кружочек внутри, значит лекция ещё грузится. ' +
            'По фиолетовой рамке можно нажать и перейти на страничку лекции. '
      }
      if (this.selectedMenuItem == 'Lections') {
        text = 'Это вкладка для загрузки лекций. ' +
            'Тут вы можете загрузить ваши аудиофайлы лекций. ' +
            'Нажмите на кнопку "Загрузите файл" что бы перейти в контенстное меню загрузки. ' +
            'Или перетащие свой файл внутри пунктирной рамки. '
      }
      if (this.selectedMenuItem == 'testfileview') {
        text = 'Это страничка вашей лекции. ' +
            'Тут вы можете просматривать текс обнаруженный в аудиофале. ' +
            'Вы можете увидеть таймкоды участка текста, для этого наведите курсор на текст. ' +
            'Так же во можете прослушать аудиофайл в специальном окне слева. '
      }
      return text
    }
  },
}
</script>

<style lang="scss" scoped>
  .header {
    border-bottom: solid 1px #D8D8D8;
    .header__body{
      margin: 20px 10px 0 20px;
      display: flex;
      flex-direction: row;
      gap: 10px;
      justify-content: space-between;
      .body__left-side {
        display: flex;
        flex-direction: row;
        gap: 10px;
        align-items: center;
        .left-side__logo {
          img {
            height: 40px;
            width: auto;
          }
        }
        .left-side__menu-button {
          img {
            height: 40px;
            width: 40px;
            cursor: pointer;
          }
         .left-side__menu-button--opened {
           img {
             height: 40px;
             width: 40px;
             cursor: pointer;
           }
         }
        }
      }
    }
    .body__right-side {
      display: flex;
      align-items: center;
      .right-side__help-ico {
        img  {
          height: 30px;
          width: auto;
          cursor: pointer;
        }
      }
    }
  }
</style>