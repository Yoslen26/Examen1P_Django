CREATE OR REPLACE PROCEDURE SP_DEL_FUTBOLISTA(
   PI_CEDULA IN VARCHAR2
)
AS
BEGIN
   UPDATE FUTBOLISTA
   SET DESCRIPCION = 'RETIRADO'
   WHERE CEDULA = PI_CEDULA;
   
   COMMIT;
END;