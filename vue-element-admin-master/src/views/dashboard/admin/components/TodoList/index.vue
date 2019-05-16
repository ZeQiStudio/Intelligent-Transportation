<template>
  <section class="todoapp">
    <!-- header -->
    <header class="header">
      <input class="new-todo" autocomplete="off" placeholder="任务列表" @keyup.enter="addTodo">
    </header>
    <!-- main section -->
    <section v-show="todos.length" class="main">
      <input
        id="toggle-all"
        :checked="allChecked"
        class="toggle-all"
        type="checkbox"
        @change="toggleAll({ done: !allChecked })"
      >
      <label for="toggle-all"/>
      <ul class="todo-list">
        <todo
          v-for="(todo, index) in filteredTodos"
          :key="index"
          :todo="todo"
          @toggleTodo="toggleTodo"
          @editTodo="editTodo"
          @deleteTodo="deleteTodo"
        />
      </ul>
    </section>
    <!-- footer -->
    <footer v-show="todos.length" class="footer">
      <span class="todo-count">
        <strong>还有{{ remaining+'个任务' }}</strong>
      </span>
      <ul class="filters">
        <li v-for="(val, key) in filters" :key="key">
          <a
            :class="{ selected: visibility === key }"
            @click.prevent="visibility = key"
          >{{ key | capitalize }}</a>
        </li>
      </ul>
      <!-- <button class="clear-completed" v-show="todos.length > remaining" @click="clearCompleted">
        Clear completed
      </button>-->
    </footer>
  </section>
</template>

<script>
import Todo from "./Todo.vue";

const STORAGE_KEY = "todos";
const filters = {
  all: todos => todos,
  active: todos => todos.filter(todo => !todo.done),
  completed: todos => todos.filter(todo => todo.done)
};
const defalutList = [
  { text: "向蜀都大道交警分队汇报路况", done: false },
  { text: "车载广播汇报路况", done: false },
  { text: "向人民中路交警分队汇报路况", done: false },
  { text: "生成当天路况数据", done: true },
  { text: "给交警大队提交任务书", done: true },
  { text: "往一环南路调配一些警力", done: true },
  { text: "疏通滨江大道二段", done: true },
  { text: "对红绿灯进行检修", done: true }
];
export default {
  components: { Todo },
  filters: {
    pluralize: (n, w) => (n === 1 ? w : w + "s"),
    capitalize: s => s.charAt(0).toUpperCase() + s.slice(1)
  },
  data() {
    return {
      visibility: "all",
      filters,
      // todos: JSON.parse(window.localStorage.getItem(STORAGE_KEY)) || defalutList
      todos: defalutList
    };
  },
  computed: {
    allChecked() {
      return this.todos.every(todo => todo.done);
    },
    filteredTodos() {
      return filters[this.visibility](this.todos);
    },
    remaining() {
      return this.todos.filter(todo => !todo.done).length;
    }
  },
  methods: {
    setLocalStorage() {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(this.todos));
    },
    addTodo(e) {
      const text = e.target.value;
      if (text.trim()) {
        this.todos.push({
          text,
          done: false
        });
        this.setLocalStorage();
      }
      e.target.value = "";
    },
    toggleTodo(val) {
      val.done = !val.done;
      this.setLocalStorage();
    },
    deleteTodo(todo) {
      this.todos.splice(this.todos.indexOf(todo), 1);
      this.setLocalStorage();
    },
    editTodo({ todo, value }) {
      todo.text = value;
      this.setLocalStorage();
    },
    clearCompleted() {
      this.todos = this.todos.filter(todo => !todo.done);
      this.setLocalStorage();
    },
    toggleAll({ done }) {
      this.todos.forEach(todo => {
        todo.done = done;
        this.setLocalStorage();
      });
    }
  }
};
</script>

<style lang="scss">
@import "./index.scss";
</style>
