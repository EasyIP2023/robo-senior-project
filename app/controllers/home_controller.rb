require 'socket'
require 'ralyxa'
class HomeController < ApplicationController
  #skip_before_action :verify_authenticity_token, only: :index

  def index
    #Ralyxa::Skill.handle(request)
  end

  def stop
    direction("Space")
    redirect_back fallback_location: root_path, notice: "Robot STOP"
  end

  def move_right
    direction("Move Right")
    redirect_back fallback_location: root_path, notice: "Moving Robot RIGHT"
  end

  def move_left
    direction("Move Left")
    redirect_back fallback_location: root_path, notice: "Moving Robot LEFT"
  end

  def move_down
    direction("Move Down")
    redirect_back fallback_location: root_path, notice: "Moving Robot DOWN"
  end

  def move_up
    direction("Move Up")
    redirect_back fallback_location: root_path, notice: "Moving Robot UP"
  end

  private

    def direction(direct)
      $sock.send(direct,0)
    end
end
