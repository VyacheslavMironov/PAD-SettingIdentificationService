<template>
  <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
    <div class="offcanvas-header">
      <h5 id="offcanvasRightLabel">Меню</h5>
      <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <div v-if="this.user_info" class="list-group mt-2">
        <a
          v-bind:href="this.server + '/profile'" 
          class="list-group-item btn"
        >Профиль</a>
      </div>
      <div v-if="this.user_info" class="list-group mt-2">
        <a
          v-if="this.user_info.role == 'Администратор'"
          href="/filial"
          class="list-group-item btn"
        >Рабочая область</a>
      </div>
      <div v-if="this.user_info" class="list-group mt-2">
        <a
          v-if="this.user_info.role == 'Директор'"
          href="/settings_working-space"
          class="list-group-item btn"
        >Настройки журнала</a>
      </div>
      <div class="list-group mt-5">
        <button
          type="button"
          v-on:click="this.logout()"
          class="list-group-item btn"
        >Выход</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: {
    server: String,
    user_info: Object
  },
  methods: {
    logout () {
      const cookies = document.cookie.split(/;/)
      for (var i = 0, len = cookies.length; i < len; i++) {
        var cookie = cookies[i].split(/=/)

        if (cookie[0] === 'user' || cookie[0] === ' user') {
          document.cookie = cookie[0] + '=;max-age=-1'
          window.location.href = '/'
        }
      }
    }
  }
}
</script>