<style>
  #signin {
    width: 30em;
    margin-top: 2em;
  }

  #signup-form {
    width: 30em;
    margin-top:2em;
  }
</style>

<template>
  <div>
    <div class="container mx-auto" v-if="!show">
      <div class="card mx-auto" id="signin">
        <h4 class="card-title text-center">Sign in</h4>
        <div class="form-label-group mx-3">
          <label for="inputEmail">Username</label>
          <input type="username" id="inputUsername" class="form-control" placeholder="Username" required autofocus v-model="username">
        </div>
        <div class="form-label-group mx-3">
          <br>
          <label for="inputPassword">Password</label>
          <input type="password" id="inputPassword" class="form-control" placeholder="Password" required v-model="password">
        </div>
        <div class="form-label-group mx-3">
          <br>
          <button type="submit" class="btn btn-primary btn-block" v-on:click="checkLogin()">SIGN IN</button>
          <button type="submit" class="btn btn-success btn-block" v-on:click="openForm()">CREATE ACCOUNT</button>
          <button type="submit" class="btn btn-secondary btn-block" v-on:click="back()">BACK TO EVENTS</button>
          <br>
        </div>
      </div>
    </div>
    <div class="row justify-content-center" v-if="show">
      <b-form @submit="onSubmit" @reset="onReset" id="signup-form">
        <div class="row">
          <div class="col-9">
            <b-form-group label="Create account"
                          label-size="lg"
                          label-class="font-weight-bold pt-0">
            </b-form-group>
          </div>
          <div class="col-3">
            <button type="button" class="close" aria-label="Close" @click="closeForm()">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        </div>
        <hr>
        <b-form-group id="input-group-1"
                      label="Username:"
                      label-for="input-1">
          <b-form-input id="input-1"
                        v-model="addUserForm.username"
                        required
                        placeholder="Enter username"></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Password:" label-for="input-2">
          <b-form-input id="input-2"
                        v-model="addUserForm.password"
                        required
                        placeholder="Enter password"
                        type="password"></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>

      </b-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      username: '',
      password: '',
      logged: false,
      is_admin: false,
      token: '',
      addUserForm: {
        username: '',
        password: ''
      },
      show: false
    }
  },

  methods: {
    checkLogin () {
      const parameters = {
        username: this.username,
        password: this.password
      }
      this.getAccount()
      const path = 'https://f1-20-eventright.herokuapp.com/login'
      axios.post(path, parameters)
        .then((res) => {
          this.logged = true
          this.token = res.data.token
          this.find_match = true
          this.$router.push({ path: '/', query: { username: this.username, logged: this.logged, is_admin: this.is_admin, token: this.token } })
          alert('The user is logged in')
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert(error.response.data.message)
        })
    },

    getAccount () {
      const path = 'https://f1-20-eventright.herokuapp.com/account/' + this.username
      axios.get(path)
        .then((res) => {
          this.is_admin = res.data.account.is_admin === 1
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },

    openForm () {
      this.show = true
      this.initForm()
    },

    closeForm () {
      this.show = false
      this.initForm()
    },

    onSubmit (evt) {
      evt.preventDefault()
      const parameters = {
        username: this.addUserForm.username,
        password: this.addUserForm.password
      }
      this.addUser(parameters)
      this.initForm()
      this.show = false
    },

    addUser (parameters) {
      const path = 'https://f1-20-eventright.herokuapp.com/account'
      axios.post(path, parameters)
        .then(() => {
          console.log('Account added')
          alert('The account has been created')
          this.username = parameters.username
          this.password = parameters.password
          this.checkLogin()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.initForm()
          alert(error.response.data.message)
        })
    },

    onReset (evt) {
      evt.preventDefault()
      // Reset our form values
      this.initForm()
    },

    initForm () {
      this.addUserForm.username = ''
      this.addUserForm.password = ''
    },

    back () {
      this.logged = false
      this.$router.push({ path: '/', query: { logged: this.logged } })
    }
  }
}
</script>
