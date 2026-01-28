from unittest.mock import Mock

from gravotech.actions.actions import GraveuseAction, LDMode


def test_graveuse_action_ad():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "AD 1"
    action = GraveuseAction(mock_streamer)
    resp = action.ad()
    assert resp == "AD 1"
    mock_streamer.write.assert_called_once_with("AD\r")


def test_graveuse_action_am():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "AM 1"
    action = GraveuseAction(mock_streamer)
    resp = action.am()
    assert resp == "AM 1"
    mock_streamer.write.assert_called_once_with("AM\r")

def test_graveuse_action_go():
    mock_streamer = Mock()
    unlock = Mock()
    mock_streamer.lock.return_value = unlock
    mock_streamer.unsafe_read.side_effect = [
        "GO M",
        "GO F",
    ]
    action = GraveuseAction(mock_streamer)
    resp = action.go()
    assert resp == "GO F"
    mock_streamer.unsafe_write.assert_called_once_with("GO")
    unlock.assert_called_once()

def test_graveuse_action_gp():
    mock_streamer = Mock()
    mock_streamer.write.return_value = 'GP "MASTER":"1"'
    action = GraveuseAction(mock_streamer)
    resp = action.gp()
    assert resp == 'GP "MASTER":"1"'
    mock_streamer.write.assert_called_once_with('GP "MASTER"\r')

def test_graveuse_action_ld():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "2\ntest.t2l\ntest2.t2l\r"
    action = GraveuseAction(mock_streamer)
    resp = action.ld("test.t2l", 1, LDMode.NORMAL)
    assert resp == "2\ntest.t2l\ntest2.t2l\r"
    mock_streamer.write.assert_called_once_with('LD "test.t2l" 1 N\r')

def test_graveuse_action_ls():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "AD 1"
    action = GraveuseAction(mock_streamer)
    resp = action.ls("*.t2l")
    assert resp == "AD 1"
    mock_streamer.write.assert_called_once_with('LS *.t2l\r')

def test_graveuse_action_pf():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "PF 1"
    action = GraveuseAction(mock_streamer)
    data = b"DEADBEEF"
    resp = action.pf("test.t2l", data)
    assert resp == "PF 1"
    mock_streamer.write.assert_called_once_with(
        f'PF "test.t2l" {data}\r'
    )


def test_graveuse_action_rm():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "RM 1"
    action = GraveuseAction(mock_streamer)
    resp = action.rm("*.t2l")
    assert resp == "RM 1"
    mock_streamer.write.assert_called_once_with("RM *.t2l\r")

def test_graveuse_action_sp():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "AD 1"
    action = GraveuseAction(mock_streamer)
    resp = action.sp(True)
    assert resp == "AD 1"
    mock_streamer.write.assert_called_once_with('SP "MASTER":"1"\r')

def test_graveuse_action_st():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "ST 4 0 0"
    action = GraveuseAction(mock_streamer)
    resp = action.st()
    assert resp == "ST 4 0 0"
    mock_streamer.write.assert_called_once_with("ST\r")

def test_graveuse_action_vg():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "example\r\n"
    action = GraveuseAction(mock_streamer)
    resp = action.vg(3)
    assert resp == "example\r\n"
    mock_streamer.write.assert_called_once_with("VG 3\r")

def test_graveuse_action_vs():
    mock_streamer = Mock()
    mock_streamer.write.return_value = "VS 1"
    action = GraveuseAction(mock_streamer)
    resp = action.vs(3, "example_vs")
    assert resp == "VS 1"
    mock_streamer.write.assert_called_once_with('VS 3 "example_vs"\r')