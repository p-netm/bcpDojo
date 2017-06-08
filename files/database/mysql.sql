SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`office`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`office` (
  `room_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`room_name`) ,
  UNIQUE INDEX `room_name_UNIQUE` (`room_name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Living_space`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`Living_space` (
  `room_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`room_name`) ,
  UNIQUE INDEX `room_name_UNIQUE` (`room_name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Persons`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`Persons` (
  `person_id` VARCHAR(8) NOT NULL ,
  `first_name` VARCHAR(75) NULL ,
  `second_name` VARCHAR(75) NULL ,
  `occupation` VARCHAR(45) NULL ,
  `office_room_name` VARCHAR(45) NULL DEFAULT 'None' ,
  `Living_space_room_name` VARCHAR(45) NULL DEFAULT 'None' ,
  PRIMARY KEY (`person_id`, `Living_space_room_name`, `office_room_name`) ,
  INDEX `fk_Persons_office_idx` (`office_room_name` ASC) ,
  INDEX `fk_Persons_Living_space1_idx` (`Living_space_room_name` ASC) ,
  CONSTRAINT `fk_Persons_office`
    FOREIGN KEY (`office_room_name` )
    REFERENCES `mydb`.`office` (`room_name` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Persons_Living_space1`
    FOREIGN KEY (`Living_space_room_name` )
    REFERENCES `mydb`.`Living_space` (`room_name` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `mydb` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

