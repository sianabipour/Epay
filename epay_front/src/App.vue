<template>
  <div class="main-app container">
    <div class="my-4">
        <img style="max-width: 200px;" src="./assets/logo.png">
    </div>
    <div class="main-body">
      <router-view></router-view>
      <hr class="my-4">
    </div>
    <h6 class="upida mb-5"><a style="color: black !important;text-decoration: none;"> طراحی شده توسط امیرحسین نبی پور</a></h6>
  </div>
</template>

<style>
textarea.form-control {
  min-height: 100px;
}
hr{
  height: 0px !important;
  border: solid 1px #17a2b8 !important;
}
.btn:hover {
  color: #fff !important;
  background-color: #17a2b8b8 !important;
  border-color: #17a2b8 !important;
}
.btn-info {
  color: #fff;
  background-color: #17a2b8;
  border-color: #17a2b8;
}
.bg-info{
  color: #fff;
  background-color: #17a2b8 !important;
  border-color: #17a2b8 !important;
}
.btn-light {
  color: #000;
  background-color: whitesmoke;
  border-color: #f8f9fa;
}
label{
  font-weight: 600;
}
body{
  direction:rtl;
  text-align:center;
}
.main-body{
  text-align: right;
  max-width: 35rem;
  margin: auto;
}
.form-control:focus {
  color: #212529;
  background-color: #fff;
  border-color: #41b883;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgb(65 189 132 / 9%);
}
.margin{
  margin-top:35px !important;
}
.button:hover{
  background-color:pink;
}
.form{
  padding: 20px;
  background: whitesmoke;
  border-radius: 20px;
  box-shadow: 4px 5px 15px 0px #c3c3c3;
}
.upida{
  margin-top:40px;
}
#page-link{
  direction:ltr;
}
.pointer{
  cursor: pointer;
}
</style>
