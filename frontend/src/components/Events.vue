<style>
  .event-card {
    width: 15em;
    margin-left: 1em;
    margin-right: 1em;
    margin-top: 1em;
    margin-bottom: 1em;
  }

  .event-info {
    font-size: 0.9em;
  }

  .bottom-card {
    margin-top: 2em;
  }

  .event-img {
    height: 10em;
  }

  #cart-column {
    vertical-align: bottom;
  }

  #event-name {
    width: 25em;
  }

  #usual-column {
    width: 15em;
  }

  tr:nth-child(even) {
    background: #d1d0de;
  }

  h1 {
    text-align: center
  }

  .top-bar {
    background-color: #808080;
    padding-top: 1em;
    padding-right: 1.5em;
  }

  .main-page {
    max-width: 100% !important;
    padding-left: 0px !important;
    padding-right: 0px !important;
  }

  .top-button {
      margin-left: 0.25em;
      margin-right: 0.25em;
  }

  .top-row {
      margin-bottom: 0.25em;
      margin-top: 0.25em;
  }

  .admin-row {
      padding-bottom: 2em;
  }

  .admin-button {
    margin-right: 0.5em;
    margin-left: 0.5em;
  }

  #addevent-form {
    width: 30em;
    margin-top: 2em;
  }

  .card-button {
      margin-top: 0.5em;
      margin-bottom: 0.5em;
  }
</style>

<template>
  <div>
    <div class="container main-page" v-if="!show">
      <div class="top-bar">
        <div class="row justify-content-end top-row">
          <b-button v-if="!is_admin && logged" class="btn btn-primary top-button" @click="showCart()">View Cart</b-button>
          <b-button v-if="is_admin && event_view" class="btn btn-primary top-button" @click="showArtists()">View Artists</b-button>
          <b-button v-if="is_admin && !event_view" class="btn btn-primary top-button" @click="showEventList()">View Events</b-button>
          <b-button class="btn btn-success top-button" @click="login()" v-if="!logged">Log in</b-button>
          <b-button class="btn btn-danger top-button" @click="logout()" v-if="logged">Log out</b-button>
        </div>
        <div class="row justify-content-end">
          <h6>Total tickets: {{ total_tickets }}</h6>
        </div>
        <div class="row justify-content-end">
          <h6>Available money: {{ money_available }}</h6>
        </div>
      </div>
      <div v-if="event_view">
        <h1>Events</h1>
        <div v-if="!addEventModal && !updateEventShow">
          <div class="row justify-content-center admin-row" v-if="is_admin">
            <button class="btn btn-success admin-button" @click="openForm()">Add New Event</button>
            <button class="btn btn-success admin-button" @click="openUpdateForm()">Update Event</button>
          </div>
          <div class="row justify-content-center">
            <div class="card text-center event-card" v-for="event in events" :key="event.id">
              <img class="card-img-top event-img" :src="getImgUrl(event.name)" :alt="event.name">
              <div class="card-body">
                <h5 class="card-title">{{ event.name }}</h5>
                <h6 v-for="artist in event.artists" :key="artist.id">{{ artist.name }}, </h6>
                <h8 v-if="is_admin">ID: {{ event.id }}<br></h8>
                <h8 class="card-text event-info">
                  {{ event.city }}<br>
                  {{ event.place }}<br>
                  {{ event.date }}<br>
                  {{ event.price }} €
                </h8>
                <div class="bottom-card">
                  <h6>Tickets available: {{ event.total_available_tickets }}</h6>
                  <b-button v-if="!is_admin && logged" class="btn btn-success card-button" @click="buyTicket(event)">Add to cart</b-button>
                  <b-button v-if="is_admin" class="card-button" variant="secondary" @click="handleAddArtist(event)">Add Artist to Event</b-button>
                  <b-button v-if="is_admin" class="card-button" variant="secondary" @click="handleDeleteArtist(event)" :disabled="event.artists.length <= 0">Delete Artist in Event</b-button>
                  <b-button v-if="is_admin" class="card-button" variant="danger" @click="removeEvent(event.id)">Delete Event</b-button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row justify-content-center" v-if="addEventModal">
          <b-form @submit="onSubmit" @reset="onReset" id="addevent-form">
            <div class="row">
              <div class="col-9">
                <b-form-group label="Add new event"
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
            <b-form-group id="input-group-1" label="Name:" label-for="input-1">
              <b-form-input id="input-1"
                            v-model="addEventForm.name"
                            required
                            placeholder="Enter event name"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Price:" label-for="input-2">
              <b-form-input id="input-2"
                            v-model="addEventForm.price"
                            required
                            placeholder="Enter price"
                            type="number"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-3" label="Date:" label-for="input-3">
              <b-form-input id="input-3"
                            v-model="addEventForm.date"
                            required
                            placeholder="Enter date"
                            type="date"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-4" label="Country:" label-for="input-4">
              <b-form-input id="input-4"
                            v-model="addEventForm.country"
                            required
                            placeholder="Enter country"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-5" label="City:" label-for="input-5">
              <b-form-input id="input-5"
                            v-model="addEventForm.city"
                            required
                            placeholder="Enter city"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-6" label="Place:" label-for="input-6">
              <b-form-input id="input-6"
                            v-model="addEventForm.place"
                            required
                            placeholder="Enter place"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-7" label="Total available tickets:" label-for="input-7">
              <b-form-input id="input-7"
                            v-model="addEventForm.total_available_tickets"
                            required
                            placeholder="Enter tickets"
                            type="number"></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
        </div>
        <div class="row justify-content-center" v-if="updateEventShow">
          <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" id="addevent-form">
            <div class="row">
              <div class="col-9">
                <b-form-group label="Update event"
                              label-size="lg"
                              label-class="font-weight-bold pt-0">
                </b-form-group>
              </div>
              <div class="col-3">
                <button type="button" class="close" aria-label="Close" @click="closeUpdateForm()">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
            </div>
            <hr>
            <b-form-group id="input-group-1" label="ID:" label-for="input-1">
              <b-form-input id="input-1"
                            v-model="editEventForm.id"
                            required
                            placeholder="Enter id"
                            type="number"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Name:" label-for="input-2">
              <b-form-input id="input-2"
                            v-model="editEventForm.name"
                            required
                            placeholder="Enter event name"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-3" label="Price:" label-for="input-3">
              <b-form-input id="input-3"
                            v-model="editEventForm.price"
                            required
                            placeholder="Enter price"
                            type="number"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-4" label="Date:" label-for="input-4">
              <b-form-input id="input-4"
                            v-model="editEventForm.date"
                            required
                            placeholder="Enter date"
                            type="date"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-5" label="Country:" label-for="input-5">
              <b-form-input id="input-5"
                            v-model="editEventForm.country"
                            required
                            placeholder="Enter country"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-6" label="City:" label-for="input-6">
              <b-form-input id="input-6"
                            v-model="editEventForm.city"
                            required
                            placeholder="Enter city"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-7" label="Place:" label-for="input-7">
              <b-form-input id="input-7"
                            v-model="editEventForm.place"
                            required
                            placeholder="Enter place"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-8" label="Total tickets available:" label-for="input-8">
              <b-form-input id="input-8"
                            v-model="editEventForm.total_available_tickets"
                            required
                            placeholder="Enter tickets"
                            type="number"></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
        </div>
      </div>
      <div v-else>
        <h1>Artists</h1>
        <div v-if="!addArtistShow && !updateArtistShow">
          <div class="row justify-content-center admin-row">
            <button class="btn btn-success admin-button" @click="openAddArtistForm()">Add New Artist</button>
            <button class="btn btn-success admin-button" @click="openUpdateArtistForm()">Update Artist</button>
          </div>
          <div class="row justify-content-center">
            <div class="card text-center event-card" v-for="artist in artists" :key="artist.id">
              <img class="card-img-top event-img" :src="getImgUrlArtist(artist.name)" :alt="artist.name">
              <div class="card-body">
                <h5 class="card-title">{{ artist.name }}</h5>
                <h8 v-if="is_admin">ID: {{ artist.id }}<br></h8>
                <h8 class="card-text event-info">
                  {{ artist.country }}<br>
                  {{ artist.genre }}
                </h8>
                <div class="bottom-card">
                  <b-button class="card-button" variant="danger" @click="removeArtist(artist.id)">Delete Artist</b-button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row justify-content-center" v-if="addArtistShow">
          <b-form @submit="onAddArtistSubmit" @reset="onAddArtistReset" id="addevent-form">
            <div class="row">
              <div class="col-9">
                <b-form-group label="Add new artist"
                              label-size="lg"
                              label-class="font-weight-bold pt-0">
                </b-form-group>
              </div>
              <div class="col-3">
                <button type="button" class="close" aria-label="Close" @click="closeAddArtistForm()">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
            </div>
            <hr>
            <b-form-group id="input-group-1" label="Name:" label-for="input-1">
              <b-form-input id="input-1"
                            v-model="addArtistForm.name"
                            required
                            placeholder="Enter artist name"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Country:" label-for="input-2">
              <b-form-input id="input-2"
                            v-model="addArtistForm.country"
                            required
                            placeholder="Enter country"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-3" label="Genre artist:" label-for="input-3">
              <b-form-select id="input-3"
                             v-model="addArtistForm.genre"
                             required
                             :options="genres">
              </b-form-select>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
        </div>
        <div class="row justify-content-center" v-if="updateArtistShow">
          <b-form @submit="onArtistSubmitUpdate" @reset="onArtistResetUpdate" id="addevent-form">
            <div class="row">
              <div class="col-9">
                <b-form-group label="Update artist"
                              label-size="lg"
                              label-class="font-weight-bold pt-0">
                </b-form-group>
              </div>
              <div class="col-3">
                <button type="button" class="close" aria-label="Close" @click="closeUpdateArtistForm()">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
            </div>
            <hr>
            <b-form-group id="input-group-1" label="ID:" label-for="input-1">
              <b-form-input id="input-1"
                            v-model="editArtistForm.id"
                            required
                            placeholder="Enter id"
                            type="number"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-1" label="Name:" label-for="input-1">
              <b-form-input id="input-1"
                            v-model="editArtistForm.name"
                            required
                            placeholder="Enter artist name"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Country:" label-for="input-2">
              <b-form-input id="input-2"
                            v-model="editArtistForm.country"
                            required
                            placeholder="Enter country"></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-3" label="Genre artist:" label-for="input-3">
              <b-form-select id="input-3"
                             v-model="editArtistForm.genre"
                             required
                             :options="genres">
              </b-form-select>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
        </div>
      </div>
    </div>
    <div class="container main-page" v-if="show">
      <div class="top-bar">
        <div class="row justify-content-end top-row">
          <button class="btn btn-primary top-button" @click="showEvents()">Back</button>
          <button class="btn btn-success top-button" @click="login()" v-if="!logged">Log in</button>
          <button class="btn btn-danger top-button" @click="logout()" v-if="logged">Log out</button>
        </div>
        <div class="row justify-content-end">
          <h6>Total tickets: {{ total_tickets }}</h6>
        </div>
        <div class="row justify-content-end">
          <h6>Available money: {{ money_available }}</h6>
        </div>
      </div>
      <h1>Cart</h1>
      <div class="row justify-content-center">
        <table v-if="this.events_added.items.length > 0">
          <thead id="cart-column">
            <tr>
              <th id="event-name">Event Name</th>
              <th id="usual-column">Quantity</th>
              <th id="usual-column">Price (€)</th>
              <th id="usual-column">Total</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in this.events_added.items" :key="item.event.id">
              <td>{{ item.event.name }}</td>
              <td>
                {{ item.quantity }}
                <button class="btn btn-danger" @click="returnTicket(item.event)">-</button>
                <button class="btn btn-success" @click="buyTicket(item.event)">+</button>
              </td>
              <td>{{ item.event.price }}</td>
              <td>{{ item.event.price * item.quantity }}</td>
              <td>
                <button class="btn btn-danger" @click="deleteTickets(item.event)">Delete tickets</button>
              </td>
            </tr>
          </tbody>
        </table>
        <h5 v-else>Your cart is currently empty</h5>
      </div>
      <div class="row justify-content-center">
        <button class="btn btn-primary btn-lg" @click="finalizePurchase()" :disabled="this.events_added.items.length <= 0">End purchase</button>
      </div>
    </div>
    <b-modal
      ref="addArtistModal"
      hide-footer
      @show="onResetAddArtistInEvent"
      @hidden="onResetAddArtistInEvent"
      title="Add artist">
      <b-form @submit.stop.prevent="onSubmitAddArtistInEvent">
        <b-form-group id="input-group-1" label="Name artist:" label-for="input-1">
          <b-form-input id="input-1"
                        v-model="addArtistEventForm.name"
                        required
                        placeholder="Enter artist name"></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Country artist:" label-for="input-2">
          <b-form-input id="input-2"
                        v-model="addArtistEventForm.country"
                        required
                        placeholder="Enter country artist"></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-3" label="Genre artist:" label-for="input-3">
          <b-form-select id="input-3"
                        v-model="addArtistEventForm.genre"
                        required
                        :options="genres"></b-form-select>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal
      ref="deleteArtistModal"
      hide-footer
      @show="onResetDeleteArtistInEvent"
      @hidden="onResetDeleteArtistInEvent"
      title="Delete artist">
      <b-form @submit.stop.prevent="onSubmitDeleteArtistInEvent">
        <b-form-group id="input-group-1" label="Name artist:" label-for="input-1">
          <b-form-input id="input-1"
                        v-model="deleteArtistForm.name"
                        required
                        placeholder="Enter artist name"></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      events: this.getEvents(),
      artists: this.getArtists(),
      events_added: { items: [] },
      show: false,
      total_tickets: 0,
      money_available: this.getMoneyAvailable(),
      username: '',
      logged: false,
      is_admin: false,
      token: '',
      event_view: true,
      addEventForm: {
        place: '',
        name: '',
        city: '',
        country: '',
        date: '',
        price: 0,
        total_available_tickets: 0
      },
      addEventModal: false,
      updateEventShow: false,
      add: false,
      editEventForm: {
        id: 0,
        place: '',
        name: '',
        city: '',
        country: '',
        date: '',
        price: 0,
        total_available_tickets: 0
      },
      event_to_modify: null,
      addArtistEventForm: {
        name: '',
        country: '',
        genre: ''
      },
      deleteArtistForm: {
        id: 0,
        name: ''
      },
      artist_id: '',
      genres: [{ value: '', text: 'Enter genre artist' }, 'REGGAE', 'POP', 'TRAP', 'HIP HOP', 'ROCK', 'INDIE', 'HEAVY', 'ELECTRONIC', 'OTHER'],
      addArtistShow: false,
      updateArtistShow: false,
      addArtistForm: {
        name: '',
        country: '',
        genre: ''
      },
      editArtistForm: {
        id: 0,
        name: '',
        country: '',
        genre: ''
      }
    }
  },

  methods: {
    buyTicket: function (event) {
      var events = []
      for (var i = 0; i < this.events_added.items.length; i++) {
        events.push(this.events_added.items[i].event.id)
      }
      if (!events.includes(event.id)) {
        this.events_added.items.push({ event, quantity: 1 })
        this.total_tickets++
      } else {
        this.events_added.items[events.indexOf(event.id)].quantity++
        this.total_tickets++
      }
    },

    returnTicket: function (event) {
      var auxEvent = this.events_added.items[0].event
      var i = 1
      while (auxEvent.id !== event.id && i < this.events_added.items.length) {
        auxEvent = this.events_added.items[i]
        i++
      }
      this.events_added.items[i - 1].quantity--
      if (this.events_added.items[i - 1].quantity <= 0) {
        this.events_added.items.splice(i - 1, 1)
      }
      this.total_tickets--
    },

    getImgUrl: function (txt) {
      try {
        return require('../assets/' + txt + '.jpg')
      } catch (e) {
        return require('../assets/default.jpg')
      }
    },

    getImgUrlArtist: function (txt) {
      try {
        return require('../assets/' + txt + '.jpg')
      } catch (e) {
        return require('../assets/default artist.jpg')
      }
    },

    deleteTickets: function (event) {
      var auxEvent = this.events_added.items[0].event
      var i = 1
      while (auxEvent.id !== event.id && i < this.events_added.items.length) {
        auxEvent = this.events_added.items[i]
        i++
      }
      this.total_tickets -= this.events_added.items[i - 1].quantity
      this.events_added.items.splice(i - 1, 1)
    },

    getEvents () {
      const path = 'https://f1-20-eventright.herokuapp.com/events'
      axios.get(path)
        .then((res) => {
          this.events = res.data.events
        })
        .catch((error) => {
          console.error(error)
          alert(error.response.data.message)
        })
    },

    showCart () {
      this.show = true
    },

    showEvents () {
      this.show = false
    },

    finalizePurchase () {
      for (let i = 0; i < this.events_added.items.length; i++) {
        const parameters = {
          id_event: this.events_added.items[i].event.id,
          tickets_bought: this.events_added.items[i].quantity
        }
        this.addPurchase(parameters)
      }
      this.events_added.items = []
      this.total_tickets = 0
    },

    addPurchase (parameters) {
      const path = 'https://f1-20-eventright.herokuapp.com/orders/' + this.username
      axios.post(path, parameters, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Order done')
          this.getMoneyAvailable()
          this.getEvents()
          this.showEvents()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          if (error.response.status === 401) {
            alert('You are not logged in or you are an admin')
          } else {
            alert(error.response.data.message)
          }
          this.getEvents()
        })
    },

    getMoneyAvailable () {
      const path = 'https://f1-20-eventright.herokuapp.com/account/' + this.username
      axios.get(path)
        .then((res) => {
          this.money_available = res.data.account.available_money
        })
        .catch((error) => {
          console.error(error)
          this.money_available = 0
        })
    },

    login () {
      this.$router.push({ path: '/userlogin' })
    },

    logout () {
      this.logged = false
      this.events_added.items = []
      this.total_tickets = 0
      this.money_available = 0
      this.username = ''
      this.is_admin = false
      this.token = ''
      this.$router.push({ path: '/' })
    },

    openForm () {
      this.addEventModal = true
      this.initForm()
    },

    closeForm () {
      this.addEventModal = false
      this.initForm()
    },

    onSubmit (evt) {
      evt.preventDefault()
      const parameters = {
        place: this.addEventForm.place,
        name: this.addEventForm.name,
        city: this.addEventForm.city,
        country: this.addEventForm.country,
        date: this.addEventForm.date,
        price: this.addEventForm.price,
        total_available_tickets: this.addEventForm.total_available_tickets
      }
      this.addEvent(parameters)
      this.initForm()
      this.addEventModal = false
    },

    addEvent (parameters) {
      const path = 'https://f1-20-eventright.herokuapp.com/event'
      axios.post(path, parameters, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Event added')
          alert('The event has been created')
          this.getEvents()
          this.$forceUpdate()
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
      this.addEventForm.place = ''
      this.addEventForm.name = ''
      this.addEventForm.city = ''
      this.addEventForm.country = ''
      this.addEventForm.date = ''
      this.addEventForm.price = 0
      this.addEventForm.total_available_tickets = 0
    },

    openUpdateForm () {
      this.updateEventShow = true
      this.initUpdateForm()
    },

    closeUpdateForm () {
      this.updateEventShow = false
      this.initUpdateForm()
    },

    onSubmitUpdate (evt) {
      evt.preventDefault()
      const parameters = {
        place: this.editEventForm.place,
        name: this.editEventForm.name,
        city: this.editEventForm.city,
        country: this.editEventForm.country,
        date: this.editEventForm.date,
        price: this.editEventForm.price,
        total_available_tickets: this.editEventForm.total_available_tickets
      }
      this.updateEvent(parameters, this.editEventForm.id)
      this.initUpdateForm()
      this.updateEventShow = false
    },

    updateEvent (parameters, id) {
      const path = 'https://f1-20-eventright.herokuapp.com/event/' + id
      axios.put(path, parameters, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Event updated')
          alert('The event has been updated')
          this.getEvents()
          this.$forceUpdate()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.initUpdateForm()
          alert(error.response.data.message)
        })
    },

    onResetUpdate (evt) {
      evt.preventDefault()
      // Reset our form values
      this.initUpdateForm()
    },

    initUpdateForm () {
      this.editEventForm.id = 0
      this.editEventForm.place = ''
      this.editEventForm.name = ''
      this.editEventForm.city = ''
      this.editEventForm.country = ''
      this.editEventForm.date = ''
      this.editEventForm.price = 0
      this.editEventForm.total_available_tickets = 0
    },

    eventWhereModifyArtist (event) {
      this.event_to_modify = event
    },

    handleAddArtist: function (event) {
      this.eventWhereModifyArtist(event)
      this.$refs.addArtistModal.show()
    },

    handleDeleteArtist: function (event) {
      this.eventWhereModifyArtist(event)
      this.$refs.deleteArtistModal.show()
    },

    onSubmitAddArtistInEvent (evt) {
      evt.preventDefault()
      this.$refs.addArtistModal.hide()
      const parameters = {
        name: this.addArtistEventForm.name,
        country: this.addArtistEventForm.country,
        genre: this.addArtistEventForm.genre
      }
      this.addNewArtist(parameters)
      this.addArtistInEvent(parameters)
      this.initAddArtistEventForm()
    },

    addNewArtist (parameters) {
      const path = 'https://f1-20-eventright.herokuapp.com/artist'
      axios.post(path, parameters, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Artist created')
          alert('The artist has been created')
          this.getArtists()
          this.$forceUpdate()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.initAddArtistEventForm()
          alert(error.response.data.message)
        })
    },

    addArtistInEvent (parameters) {
      const path = 'https://f1-20-eventright.herokuapp.com/event/' + this.event_to_modify.id + '/artist'
      axios.post(path, parameters, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Artist added')
          alert('The artist has been added to event')
          this.getEvents()
          this.$forceUpdate()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.initAddArtistEventForm()
          alert(error.response.data.message)
        })
    },

    onResetAddArtistInEvent () {
      this.initAddArtistEventForm()
    },

    initAddArtistEventForm () {
      this.addArtistEventForm.name = ''
      this.addArtistEventForm.country = ''
      this.addArtistEventForm.genre = ''
    },

    onSubmitDeleteArtistInEvent (evt) {
      evt.preventDefault()
      this.$refs.deleteArtistModal.hide()
      var i = 0
      this.artist_id = 0
      while (i < this.event_to_modify.artists.length && this.artist_id === 0) {
        if (this.event_to_modify.artists[i].name === this.deleteArtistForm.name) {
          this.artist_id = this.event_to_modify.artists[i].id
        }
        i++
      }
      if (this.artist_id === 0) {
        alert('Artist not found')
      } else {
        this.deleteArtistInEvent()
      }
    },

    onResetDeleteArtistInEvent () {
      this.initDeleteArtistForm()
    },

    deleteArtistInEvent () {
      const path = 'https://f1-20-eventright.herokuapp.com/event/' + this.event_to_modify.id + '/artist/' + this.artist_id
      axios.delete(path, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Artist deleted from event')
          alert('The artist has been deleted from the event')
          this.getEvents()
          this.$forceUpdate()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.initDeleteArtistForm()
          alert(error.response.data.message)
        })
    },

    initDeleteArtistForm () {
      this.deleteArtistForm.id = 0
      this.deleteArtistForm.name = ''
    },

    removeEvent (eventid) {
      const path = 'https://f1-20-eventright.herokuapp.com/event/' + eventid
      axios.delete(path, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Event removed')
          alert('The event has been removed')
          this.getEvents()
          this.$forceUpdate()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          alert(error.response.data.message)
        })
    },

    showArtists () {
      this.event_view = false
    },

    showEventList () {
      this.event_view = true
    },

    getArtists () {
      const path = 'https://f1-20-eventright.herokuapp.com/artists'
      axios.get(path)
        .then((res) => {
          this.artists = res.data.artists
        })
        .catch((error) => {
          console.error(error)
          alert(error.response.data.message)
        })
    },

    openAddArtistForm () {
      this.addArtistShow = true
      this.initAddArtistForm()
    },

    closeAddArtistForm () {
      this.addArtistShow = false
      this.initAddArtistForm()
    },

    onAddArtistSubmit (evt) {
      evt.preventDefault()
      const parameters = {
        name: this.addArtistForm.name,
        country: this.addArtistForm.country,
        genre: this.addArtistForm.genre
      }
      this.addArtist(parameters)
      this.initAddArtistForm()
      this.addArtistShow = false
    },

    addArtist (parameters) {
      const path = 'https://f1-20-eventright.herokuapp.com/artist'
      axios.post(path, parameters, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Artist added')
          alert('The artist has been created')
          this.getArtists()
          this.$forceUpdate()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.initAddArtistForm()
          alert(error.response.data.message)
        })
    },

    onAddArtistReset (evt) {
      evt.preventDefault()
      // Reset our form values
      this.initAddArtistForm()
    },

    initAddArtistForm () {
      this.addArtistForm.name = ''
      this.addArtistForm.country = ''
      this.addArtistForm.genre = ''
    },

    openUpdateArtistForm () {
      this.updateArtistShow = true
      this.initUpdateArtistForm()
    },

    closeUpdateArtistForm () {
      this.updateArtistShow = false
      this.initUpdateArtistForm()
    },

    onArtistSubmitUpdate (evt) {
      evt.preventDefault()
      const parameters = {
        name: this.editArtistForm.name,
        country: this.editArtistForm.country,
        genre: this.editArtistForm.genre
      }
      this.updateArtist(parameters, this.editArtistForm.id)
      this.initUpdateArtistForm()
      this.updateArtistShow = false
    },

    updateArtist (parameters, id) {
      const path = 'https://f1-20-eventright.herokuapp.com/artist/' + id
      axios.put(path, parameters, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Artist updated')
          alert('The artist has been updated')
          this.getArtists()
          this.$forceUpdate()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.initUpdateArtistForm()
          alert(error.response.data.message)
        })
    },

    onArtistResetUpdate (evt) {
      evt.preventDefault()
      // Reset our form values
      this.initUpdateArtistForm()
    },

    initUpdateArtistForm () {
      this.editArtistForm.id = 0
      this.editArtistForm.name = ''
      this.editArtistForm.country = ''
      this.editArtistForm.genre = ''
    },

    removeArtist (artistid) {
      const path = 'https://f1-20-eventright.herokuapp.com/artist/' + artistid
      axios.delete(path, {
        auth: { username: this.token }
      })
        .then(() => {
          console.log('Artist removed')
          alert('The artist has been removed')
          this.getArtists()
          this.getEvents()
          this.$forceUpdate()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          alert(error.response.data.message)
        })
    }
  },

  created () {
    this.getEvents()
    this.getArtists()
    this.logged = this.$route.query.logged
    this.username = this.$route.query.username
    this.is_admin = this.$route.query.is_admin
    this.token = this.$route.query.token
    this.getMoneyAvailable()
  }
}
</script>
