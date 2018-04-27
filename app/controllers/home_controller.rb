require 'socket'
require 'ralyxa'
class HomeController < ApplicationController
  #skip_before_action :verify_authenticity_token, only: :index

  def index
    #Ralyxa::Skill.handle(request)
  end

  def stop
    direction("WebApp,Space")
    redirect_back fallback_location: root_path, notice: "Robot STOP"
  end

  def move_right
    direction("WebApp,Move Right")
    redirect_back fallback_location: root_path, notice: "Moving Robot RIGHT"
  end

  def move_left
    direction("WebApp,Move Left")
    redirect_back fallback_location: root_path, notice: "Moving Robot LEFT"
  end

  def move_down
    direction("WebApp,Move Down")
    redirect_back fallback_location: root_path, notice: "Moving Robot DOWN"
  end

  def move_up
    direction("WebApp,Move Up")
    redirect_back fallback_location: root_path, notice: "Moving Robot UP"
  end

  private

    def direction(direct)
      $sock.send(direct,0)
    end
end
