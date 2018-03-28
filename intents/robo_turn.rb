intent "RoboTurn" do
  movements = ['forward','back','left','right'].each do |move|
    move_slot = request.slot_value(move)
    move_slot ? movements + [move_slot] : movements
  end

  unless movements.nil?
    case movements[1]
    when 'forward'
      $sock.send("Move Up",0)
      ask("Moving Robot #{movements[1]}")
    when 'back'
      $sock.send("Move Down",0)
      ask("Moving Robot #{movements[1]}")
    when 'left'
      $sock.send("Move Left",0)
      ask("Turning Robot #{movements[1]}")
    when 'right'
      $sock.send("Move Right",0)
      ask("Turning Robot #{movements[1]}")
    else
      ask("No command was found please try again")
    end
  end
end
