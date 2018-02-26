require 'socket'
class HomeController < ApplicationController
  def index
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

    # TODO Come up with a better way to get this to work with epoll
    def direction(direct)
      Thread.new {
        sock = TCPSocket.open Socket.gethostname, 8080
        sock.send(direct,0)
        sock.close
      }
    end
end
