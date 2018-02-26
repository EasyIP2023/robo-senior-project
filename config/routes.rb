Rails.application.routes.draw do

  namespace :home do
    get :move_right
    get :move_left
    get :move_down
    get :move_up
    get :stop
  end

  root 'home#index'
end
