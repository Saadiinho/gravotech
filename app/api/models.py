from pydantic import BaseModel, Field

from libs.actions.actions import LDMode


class LoadFile(BaseModel):
    """
    Schema for loading a marking file (LD command).

    :ivar filename: Name of the file to be loaded for marking. [cite: 490]
    :vartype filename: str
    :ivar nb_marking: Number of marking cycles (0 to 4294967295; 0 for infinite/autonomous). [cite: 490]
    :vartype nb_marking: int
    :ivar mode: Marking mode execution (Normal, Simulation, or Autonomous). [cite: 490]
    :vartype mode: LDMode
    """

    filename: str
    nb_marking: int
    mode: LDMode


class Mask(BaseModel):
    """
    Schema for file filtering operations (LS or RM commands).

    :ivar mask: Search pattern or filename (e.g., "*.t21", "test.po3"). [cite: 495, 647]
    :vartype mask: str
    """

    mask: str


class PushFile(BaseModel):
    """
    Schema for uploading a file to the machine (PF command).

    :ivar filename: Target name for the file on the machine's memory. [cite: 613]
    :vartype filename: str
    :ivar data: Hexadecimal byte representation of the file content. [cite: 613]
    :vartype data: bytes
    """

    filename: str
    data: bytes


class Rule(BaseModel):
    """
    Schema for modifying the connection privilege (SP command).

    :ivar rule: True to request Master status ("1"), False for Slave status ("0"). [cite: 679]
    :vartype rule: bool
    """

    rule: bool


class GetValue(BaseModel):
    """
    Schema for requesting a specific variable value (VG command).

    :ivar index: The variable index number (typically 0 to 9). [cite: 702]
    :vartype index: int
    """

    index: int


class SetValue(BaseModel):
    """
    Schema for assigning text to a machine variable (VS command).

    :ivar index: The variable index number to update (0 to 9). [cite: 775]
    :vartype index: int
    :ivar text: The UTF-8 text string to store in the variable. [cite: 778]
    :vartype text: str
    """

    index: int
    text: str


class Response(BaseModel):
    """
    Standard generic response wrapper for machine actions.

    :ivar response: The raw or decoded string response from the machine. [cite: 69, 70]
    :vartype response: str
    """

    response: str


class HealthcheckResponse(BaseModel):
    """
    Schema for the API health status check.

    :ivar name: The name of the API service.
    :vartype name: str
    :ivar status: Current availability status (e.g., "OK").
    :vartype status: str
    :ivar version: The semantic versioning string of the application.
    :vartype version: str
    """

    name: str
    status: str
    version: str
