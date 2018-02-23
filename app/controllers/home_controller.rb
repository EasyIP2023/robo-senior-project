require 'socket'
class HomeController < ApplicationController
  def index
  end

  def move_right
    redirect_to root_path, notice: "Moving Robot Right"
  end

  def move_left
    redirect_to root_path, notice: "Moving Robot Left"
  end

  def move_down
    redirect_to root_path, notice: "Moving Robot Down"
  end

  def move_up
    redirect_to root_path, notice: "Moving Robot Up"
  end
end
