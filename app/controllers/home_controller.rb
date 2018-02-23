require 'socket'
class HomeController < ApplicationController
  def index
  end

  def move_right
    redirect_back fallback_location: root_path, notice: "Moving Robot Right"
  end

  def move_left
    redirect_back fallback_location: root_path, notice: "Moving Robot Left"
  end

  def move_down
    redirect_back fallback_location: root_path, notice: "Moving Robot Down"
  end

  def move_up
    redirect_back fallback_location: root_path, notice: "Moving Robot Up"
  end
end
